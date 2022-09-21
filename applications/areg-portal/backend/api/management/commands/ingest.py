import itertools
import logging
import math
import string
from timeit import default_timer as timer

import pandas as pd
from django.core.management.base import BaseCommand
from django.db import transaction, connection

from api.management.pre_process import preprocess
from api.models import STATUS, CommercialType, AntibodyClonality, Antibody, Antigen, Vendor, VendorDomain, Specie, \
    VendorSynonym, AntibodySpecies

TRUNCATE_STM = "TRUNCATE TABLE {table_name} CASCADE;"
INSERT_INTO_VALUES_STM = "INSERT INTO {table_name} ({columns}) VALUES {} ;"
DROP_TABLE_STM = "DROP TABLE IF EXISTS {table_name} ;"
CREATE_TABLE_STM = "CREATE TABLE {table_name} ({columns}) ; "
INSERT_INTO_SELECT_STM = "INSERT INTO {to_table_name} ({to_columns}) SELECT {distinct} {from_columns} FROM {from_table_name};"


def get_create_table_stm(table_name, columns):
    columns_str = ", ".join([f"{column} text" for column in columns])
    return CREATE_TABLE_STM.format(table_name=table_name, columns=columns_str)


def get_insert_into_table_select_stm(to_table_name, to_columns, distinct, from_columns, from_table_name):
    distinct_str = 'DISTINCT' if distinct else ''
    return INSERT_INTO_SELECT_STM.format(to_table_name=to_table_name, to_columns=to_columns, distinct=distinct_str,
                                         from_columns=from_columns, from_table_name=from_table_name)


def get_insert_values_into_table_stm(table_name, columns, entries):
    return INSERT_INTO_VALUES_STM.format(
        ', '.join([f"({', '.join(['%s' for _ in range(0, len(columns))])})"] * entries), table_name=table_name,
        columns=', '.join(columns))


def clean_empty_value(value):
    if is_null_value(value):
        return None
    return value


def is_null_value(value):
    return value == '(null)' or value == '(NaN)' or (
                type(value) == float and math.isnan(value)) or value == 'null' or value is None


def handle_undefined_commercial_type(value):
    if value not in CommercialType.labels:
        return None
    return value


def get_clean_species_str(specie: str):
    return specie.translate(str.maketrans('', '', string.punctuation)).strip().lower()


class Command(BaseCommand):
    ANTIBODY_TABLE = Antibody.objects.model._meta.db_table
    ANTIGEN_TABLE = Antigen.objects.model._meta.db_table
    SPECIE_TABLE = Specie.objects.model._meta.db_table
    VENDOR_DOMAIN_TABLE = VendorDomain.objects.model._meta.db_table
    VENDOR_SYNONYM_TABLE = VendorSynonym.objects.model._meta.db_table
    VENDOR_TABLE = Vendor.objects.model._meta.db_table
    TMP_TABLE = 'tmp_table'

    help = "Ingests antibody data into the database"

    def add_arguments(self, parser):
        parser.add_argument("file_id", type=str)

    def handle(self, *args, **options):

        # Pre process google drive data
        metadata = preprocess(options["file_id"])

        commercial_type_reverse_map = {value: key for key, value in CommercialType.choices}
        status_reverse_map = {value.upper(): key for key, value in STATUS.choices}
        clonality_reverse_map = {value.lower(): key for key, value in AntibodyClonality.choices}

        # Prepare vendor inserts
        df_vendor = pd.read_csv(metadata.vendor_data_path)
        vendor_insert_stm = get_insert_values_into_table_stm(self.VENDOR_TABLE,
                                                             ['id', 'nif_id', 'vendor'],
                                                             len(df_vendor))

        # Prepare vendor domain inserts
        df_vendor_domain = pd.read_csv(metadata.vendor_domain_data_path)
        df_vendor_domain = df_vendor_domain.drop_duplicates(subset=["domain_name"])
        vendor_domain_insert_stm = get_insert_values_into_table_stm(self.VENDOR_DOMAIN_TABLE,
                                                                    ['id', 'domain_name', 'vendor_id', 'status',
                                                                     'link'],
                                                                    len(df_vendor_domain))

        # Prepare raw antibody inserts
        header = ['ab_name', 'ab_target', 'target_species', 'vendor', 'vendor_id', 'catalog_num', 'clonality',
                  'source_organism', 'clone_id', 'url', 'link', 'ab_target_entrez_gid', 'product_isotype',
                  'product_conjugate', 'product_form', 'target_subregion', 'target_modification', 'comments',
                  'feedback', 'defining_citation', 'disc_date', 'curator_comment', 'id', 'ab_id', 'ab_id_old',
                  'of_record', 'ix', 'uid', 'status', 'insert_time', 'curate_time', 'cat_alt', 'commercial_type',
                  'uniprot_id', 'epitope'
                  ]

        start = timer()
        logging.info("Ingestion process started")

        with transaction.atomic():
            with connection.cursor() as cursor:
                # delete tables content (opposite order of insertion)
                tables_to_delete = [self.SPECIE_TABLE, self.ANTIBODY_TABLE,
                                    self.ANTIGEN_TABLE, self.VENDOR_SYNONYM_TABLE,
                                    self.VENDOR_DOMAIN_TABLE, self.VENDOR_TABLE]
                for ttd in tables_to_delete:
                    cursor.execute(TRUNCATE_STM.format(table_name=ttd))

                # insert vendors
                vendor_synonyms_params = []
                vendor_params = []
                for index, row in df_vendor.iterrows():
                    vendor_params.extend(
                        [row['id'], clean_empty_value(row['nifID']), row['vendor']])
                    synonyms_str = clean_empty_value(row['synonym'])
                    if synonyms_str:
                        for s in synonyms_str.split(','):
                            vendor_synonyms_params.extend([row['id'], s])

                cursor.execute(vendor_insert_stm, vendor_params)

                # insert vendors synonyms
                vendor_synonyms_insert_stm = get_insert_values_into_table_stm(
                    self.VENDOR_SYNONYM_TABLE,
                    ['vendor_id', 'name'],
                    int(len(vendor_synonyms_params) / 2))
                cursor.execute(vendor_synonyms_insert_stm, vendor_synonyms_params)

                # insert vendors domains
                vendor_domain_params = []
                for index, row in df_vendor_domain.iterrows():
                    vendor_domain_params.extend(
                        [row['id'], row['domain_name'], row['vendor_id'],
                         status_reverse_map[row['status'].upper()], False])
                cursor.execute(vendor_domain_insert_stm, vendor_domain_params)

                # Create copy table
                cursor.execute(get_create_table_stm(self.TMP_TABLE, header))

                # Insert raw data into tmp table
                for chunk in pd.read_csv(metadata.antibody_data_path, chunksize=10 ** 4, dtype='unicode'):
                    raw_data_insert_stm = get_insert_values_into_table_stm(self.TMP_TABLE, header, len(chunk))
                    row_params = []
                    for index, row in chunk.iterrows():
                        try:
                            row['commercial_type'] = commercial_type_reverse_map[row['commercial_type']]
                        except KeyError:
                            row['commercial_type'] = None
                        row['status'] = status_reverse_map[row['status']]
                        row['clonality'] = clonality_reverse_map.get(row['clonality'].lower(), 'UNK') if type(
                            row['clonality']) != float else 'UNK'
                        row_params.extend([clean_empty_value(value) for value in row.values])
                    cursor.execute(raw_data_insert_stm, row_params)

                # Insert select distinct antigen

                cursor.execute(get_insert_into_table_select_stm(self.ANTIGEN_TABLE,
                                                                'ab_target',
                                                                True,
                                                                'ab_target',
                                                                self.TMP_TABLE))
                # Update antigen with ids
                # todo: Update according to https://github.com/MetaCell/scicrunch-antibody-registry/issues/65
                antigen_update_stm = f"UPDATE {self.ANTIGEN_TABLE} " \
                                     f"SET ab_target_entrez_gid=TMP.ab_target_entrez_gid, " \
                                     f"uniprot_id=TMP.uniprot_id " \
                                     f"FROM {self.TMP_TABLE} as TMP " \
                                     f"WHERE {self.ANTIGEN_TABLE}.ab_target=TMP.ab_target; "
                cursor.execute(antigen_update_stm)

                # Insert into antibody

                antibody_stm = f"INSERT INTO {self.ANTIBODY_TABLE} (ix, ab_name, ab_id, accession, commercial_type, uid, catalog_num, cat_alt, " \
                               f"vendor_id, url, antigen_id, target_subregion, target_modification, " \
                               f"epitope, clonality, clone_id, product_isotype, " \
                               f"product_conjugate, defining_citation, product_form, comments, feedback, " \
                               f"curator_comment, disc_date, status, insert_time, curate_time)" \
                               f"SELECT DISTINCT CAST(ix as BIGINT), ab_name, CAST(ab_id as INT), ab_id_old, commercial_type, " \
                               f"uid, catalog_num, cat_alt, CAST(vendor_id as BIGINT), url, antigen.id, " \
                               f"target_subregion, target_modification, epitope, clonality, " \
                               f"clone_id, product_isotype, product_conjugate, defining_citation, product_form, " \
                               f"comments, feedback, curator_comment, disc_date, status, " \
                               f"to_timestamp(cast(insert_time as BIGINT) / 1000000.0), " \
                               f"to_timestamp(cast(curate_time as BIGINT) / 1000000.0) " \
                               f"FROM {self.TMP_TABLE} as tmp " \
                               f"JOIN {self.VENDOR_TABLE} as vendor " \
                               f"ON CAST(tmp.vendor_id AS integer) = vendor.id " \
                               f"JOIN {self.ANTIGEN_TABLE} as antigen " \
                               f"ON tmp.ab_target = antigen.ab_target;"

                cursor.execute(antibody_stm)

                # Insert into species

                get_species_stm = f"SELECT DISTINCT target_species FROM {self.TMP_TABLE} " \
                                  f"UNION " \
                                  f"SELECT DISTINCT source_organism FROM {self.TMP_TABLE}"
                cursor.execute(get_species_stm)
                species_map = {}
                species_id = 1
                for row in cursor:
                    specie_str = row[0]
                    if specie_str:
                        for specie in specie_str.split(';'):
                            clean_specie = get_clean_species_str(specie)
                            if clean_specie not in species_map:
                                species_map[clean_specie] = species_id
                                species_id += 1
                species_insert_stm = get_insert_values_into_table_stm(self.SPECIE_TABLE,
                                                                      ['name', 'id'],
                                                                      len(species_map.keys()))
                cursor.execute(species_insert_stm, list(itertools.chain.from_iterable(species_map.items())))

                # Insert into antibody species

                for chunk in pd.read_csv(metadata.antibody_data_path, chunksize=10 ** 4, dtype='unicode'):
                    species_params = []
                    for index, row in chunk.iterrows():
                        target_species = row['target_species']
                        if not is_null_value(target_species):
                            for specie in row['target_species'].split(';'):
                                clean_specie = get_clean_species_str(specie)
                                species_params.extend([row['ix'], species_map[clean_specie]])

                antibody_species_insert_stm = get_insert_values_into_table_stm(
                    AntibodySpecies.objects.model._meta.db_table, ['antibody_id', 'specie_id'],
                    int(len(species_params) / 2))

                cursor.execute(antibody_species_insert_stm, species_params)

                # Update antibody source_organism

                source_organism_update_stm = f"UPDATE {self.ANTIBODY_TABLE} " \
                                             f"SET source_organism_id=SP.id " \
                                             f"FROM {self.SPECIE_TABLE} as SP " \
                                             f"JOIN {self.TMP_TABLE} as TP " \
                                             f"ON lower(TP.source_organism) = SP.name " \
                                             f"WHERE CAST(TP.ix AS integer)={self.ANTIBODY_TABLE}.ix "

                cursor.execute(source_organism_update_stm)

                # Update vendor domain link
                antigen_update_stm = f"UPDATE {self.VENDOR_DOMAIN_TABLE} " \
                                     f"SET link = True " \
                                     f"FROM {self.TMP_TABLE} " \
                                     f"WHERE {self.VENDOR_DOMAIN_TABLE}.vendor_id=CAST({self.TMP_TABLE}.vendor_id as BIGINT) " \
                                     f"AND lower({self.TMP_TABLE}.link) = 'yes'; "
                cursor.execute(antigen_update_stm)

                # Drop tmp table
                cursor.execute(DROP_TABLE_STM.format(table_name=self.TMP_TABLE))

        end = timer()
        logging.info(f"Ingestion finished in {end - start} seconds")
