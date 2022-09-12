import logging
import math
from timeit import default_timer as timer

import pandas as pd
from django.core.management.base import BaseCommand
from django.db import transaction, connection

from api.models import STATUS, CommercialType, AntibodyClonality

TRUNCATE_STM = "TRUNCATE TABLE $tableName CASCADE;"
INSERT_INTO_VALUES_STM = "INSERT INTO $tableName ($columns) VALUES {} ;"
DROP_TABLE_STM = "DROP TABLE IF EXISTS $tableName ;"
CREATE_TABLE_STM = "CREATE TABLE $tableName ($columns) ; "
INSERT_INTO_SELECT_STM = "INSERT INTO $toTableName ($toColumns) SELECT $distinct $fromColumns FROM $fromTableName ;"


def get_create_table_stm(table_name, columns):
    columns_str = ", ".join([f"{column} text" for column in columns])
    return CREATE_TABLE_STM.replace('$tableName', table_name) \
        .replace('$columns', columns_str)


def get_insert_into_table_select_stm(to_table_name, to_columns, distinct, from_columns, from_table_name):
    distinct_str = 'DISTINCT' if distinct else ''
    return INSERT_INTO_SELECT_STM \
        .replace('$toTableName', to_table_name) \
        .replace('$toColumns', ', '.join(to_columns)) \
        .replace('$distinct', distinct_str) \
        .replace('$fromColumns', ', '.join(from_columns)) \
        .replace('$fromTableName', from_table_name)


def get_insert_values_into_table_stm(table_name, columns, entries):
    return INSERT_INTO_VALUES_STM.replace('$tableName', table_name).replace('$columns', ', '.join(columns)).format(
        ', '.join([f"({', '.join(['%s' for _ in range(0, len(columns))])})"] * entries))


def clean_empty_value(value):
    if value == '(null)' or value == '(NaN)' or (type(value) == float and math.isnan(value)) or value is None:
        return ''
    return value


def handle_undefined_commercial_type(value):
    # todo: handle accordingly to https://github.com/MetaCell/scicrunch-antibody-registry/issues/53
    if value not in CommercialType.labels:
        return 'other'
    return value


class Command(BaseCommand):
    help = "Ingests antibody data into the database"

    def add_arguments(self, parser):
        parser.add_argument("antibody_table_uri", type=str)
        parser.add_argument("vendor_table_uri", type=str)
        parser.add_argument("vendor_domain_table_uri", type=str)

    def handle(self, *args, **options):

        commercial_type_reverse_map = {value: key for key, value in CommercialType.choices}
        status_reverse_map = {value: key for key, value in STATUS.choices}
        clonality_reverse_map = {value.lower(): key for key, value in AntibodyClonality.choices}

        # Prepare vendor inserts
        df_vendor = pd.read_csv(options['vendor_table_uri'])
        vendor_insert_stm = get_insert_values_into_table_stm('api_vendor',
                                                             ['id', 'nif_id', 'vendor', 'synonyms', 'commercial_type'],
                                                             len(df_vendor))

        # Prepare vendor domain inserts
        df_vendor_domain = pd.read_csv(options['vendor_domain_table_uri'])
        df_vendor_domain = df_vendor_domain.drop_duplicates(subset=["domain_name"])
        vendor_domain_insert_stm = get_insert_values_into_table_stm('api_vendordomain',
                                                                    ['id', 'domain_name', 'vendor_id', 'status',
                                                                     'link'],
                                                                    len(df_vendor_domain))

        # Prepare raw antibody inserts
        tmp_table_name = 'tmp_table'
        header = ['ab_name', 'ab_target', 'target_species', 'vendor', 'vendor_id', 'catalog_num', 'clonality',
                  'source_organism', 'clone_id', 'url', 'link', 'ab_target_entrez_gid', 'product_isotype',
                  'product_conjugate', 'product_form', 'target_subregion', 'target_modification', 'comments',
                  'feedback', 'defining_citation', 'disc_date', 'curator_comment', 'id', 'ab_id', 'ab_id_old',
                  'of_record', 'ix', 'uid', 'status', 'insert_time', 'curate_time', 'cat_alt', 'commercial_type',
                  'uniprot_id', 'epitope'
                  ]

        start = timer()

        with transaction.atomic():
            with connection.cursor() as cursor:
                # delete tables content (opposite order of insertion)
                # todo: do we need all the executes or just 1 with cascade?
                tables_to_delete = ['api_antibody', 'api_antigen', 'api_vendor', 'api_vendordomain']
                for ttd in tables_to_delete:
                    cursor.execute(TRUNCATE_STM.replace('$tableName', ttd))

                # insert vendors
                vendor_params = []
                for index, row in df_vendor.iterrows():
                    vendor_params.extend(
                        [row['id'], clean_empty_value(row['nifID']), row['vendor'], clean_empty_value(row['synonym']),
                         commercial_type_reverse_map[handle_undefined_commercial_type(row['commercial_type'])]])
                cursor.execute(vendor_insert_stm, vendor_params)

                # insert vendors domains
                # todo: Handle bad references according to https://github.com/MetaCell/scicrunch-antibody-registry/issues/54
                vendor_domain_params = []
                for index, row in df_vendor_domain.iterrows():
                    vendor_domain_params.extend(
                        [row['id'], row['domain_name'], row['vendor_id'],
                         status_reverse_map[row['status']], False])
                cursor.execute(vendor_domain_insert_stm, vendor_domain_params)

                # Create copy table
                cursor.execute(DROP_TABLE_STM.replace('$tableName', tmp_table_name))
                cursor.execute(get_create_table_stm(tmp_table_name, header))

                # Insert raw data into tmp table
                for chunk in pd.read_csv(options['antibody_table_uri'], chunksize=10 ** 4, dtype='unicode'):
                    raw_data_insert_stm = get_insert_values_into_table_stm(tmp_table_name, header, len(chunk))
                    # todo: format species string into a more rigid format (csv or semicolon separated values + order)
                    # https://github.com/MetaCell/scicrunch-antibody-registry/issues/55
                    row_params = []
                    for index, row in chunk.iterrows():
                        row['status'] = status_reverse_map[row['status']]
                        row['clonality'] = clonality_reverse_map.get(row['clonality'].lower(), 'UNK') if type(
                            row['clonality']) != float else 'UNK'
                        row_params.extend([clean_empty_value(value) for value in row.values])
                    cursor.execute(raw_data_insert_stm, row_params)

                # Insert select distinct antigen
                cursor.execute(get_insert_into_table_select_stm('api_antigen',
                                                                ['ab_target'],
                                                                True,
                                                                ['ab_target'],
                                                                tmp_table_name))
                # Update antigen with ids

                antigen_update_stm = "UPDATE api_antigen " \
                                     "SET ab_target_entrez_gid=TMP.ab_target_entrez_gid, " \
                                     "uniprot_id=TMP.uniprot_id " \
                                     "FROM tmp_table TMP " \
                                     "WHERE api_antigen.ab_target=TMP.ab_target; "
                cursor.execute(antigen_update_stm)

                # Insert into antibody

                antibody_stm = f"INSERT INTO api_antibody (ix, ab_name, ab_id, accession, uid, catalog_num, cat_alt, " \
                               f"vendor_id, url, antigen_id, target_species, target_subregion, target_modification, " \
                               f"epitope, source_organism, clonality, clone_id, product_isotype, " \
                               f"product_conjugate, defining_citation, product_form, comments, feedback, " \
                               f"curator_comment, disc_date, status, insert_time, curate_time)" \
                               f"SELECT DISTINCT CAST(ix as BIGINT), ab_name, ab_id, ab_id_old, uid, catalog_num, " \
                               f"cat_alt, CAST(vendor_id as BIGINT), url, api_antigen.id, target_species, " \
                               f"target_subregion, target_modification, epitope,source_organism, clonality, " \
                               f"clone_id, product_isotype, product_conjugate, defining_citation, product_form, " \
                               f"comments, feedback, curator_comment, disc_date, status, " \
                               f"to_timestamp(cast(insert_time as BIGINT) / 1000000.0), " \
                               f"to_timestamp(cast(curate_time as BIGINT) / 1000000.0) " \
                               f"FROM {tmp_table_name}, api_vendor, api_antigen " \
                               f"WHERE {tmp_table_name}.vendor_id = CAST(api_vendor.id AS text) AND " \
                               f"{tmp_table_name}.ab_target = api_antigen.ab_target;"

                cursor.execute(antibody_stm)

                # Update vendor domain link
                antigen_update_stm = "UPDATE api_vendordomain " \
                                     "SET link = True " \
                                     "FROM tmp_table " \
                                     "WHERE api_vendordomain.vendor_id=CAST(tmp_table.vendor_id as BIGINT) " \
                                     "AND lower(tmp_table.link) = 'yes'; "
                cursor.execute(antigen_update_stm)

        end = timer()
        logging.info(f"Ingestion finished in {end - start} seconds")
