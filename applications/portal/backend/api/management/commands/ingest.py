import itertools
import logging
import string
from timeit import default_timer as timer

import pandas as pd
from django.core.management.base import BaseCommand
from django.core.management.color import no_style
from django.db import transaction, connection

from api.management.pre_process import preprocess
from api.models import Antibody, Gene, Vendor, VendorDomain, Specie, \
    VendorSynonym, AntibodySpecies
from areg_portal.settings import ANTIBODY_ANTIBODY_START_SEQ, ANTIBODY_VENDOR_START_SEQ, \
    ANTIBODY_VENDOR_DOMAIN_START_SEQ, ANTIBODY_HEADER
from areg_portal.settings import CHUNK_SIZE

TRUNCATE_STM = "TRUNCATE TABLE {table_name} CASCADE;"
INSERT_INTO_VALUES_STM = "INSERT INTO {table_name} ({columns}) VALUES {} ;"
DROP_TABLE_STM = "DROP TABLE IF EXISTS {table_name} ;"
CREATE_TABLE_STM = "CREATE TABLE {table_name} ({columns}) ; "
INSERT_INTO_SELECT_STM = "INSERT INTO {to_table_name} ({to_columns}) SELECT {distinct} {from_columns} FROM {from_table_name};"
RESTART_SEQ_STM = "ALTER SEQUENCE {table_name} RESTART WITH {value};"


def get_restart_seq_stm(table_name, value):
    return RESTART_SEQ_STM.format(table_name=table_name, value=value)


def get_create_table_stm(table_name, columns_dict):
    columns_str = ", ".join([f"{column} {columns_dict[column]}" for column in columns_dict])
    return CREATE_TABLE_STM.format(table_name=table_name, columns=columns_str)


def get_insert_into_table_select_stm(to_table_name, to_columns, distinct, from_columns, from_table_name):
    distinct_str = 'DISTINCT' if distinct else ''
    return INSERT_INTO_SELECT_STM.format(to_table_name=to_table_name, to_columns=to_columns, distinct=distinct_str,
                                         from_columns=from_columns, from_table_name=from_table_name)


def get_insert_values_into_table_stm(table_name, columns, entries):
    return INSERT_INTO_VALUES_STM.format(
        ', '.join([f"({', '.join(['%s' for _ in range(0, len(columns))])})"] * entries),
        table_name=table_name,
        columns=', '.join(columns))

def get_clean_species_str(specie: str):
    return specie.translate(str.maketrans('', '', string.punctuation)).strip().lower()


class Command(BaseCommand):
    ANTIBODY_TABLE = Antibody.objects.model._meta.db_table
    ANTIGEN_TABLE = Gene.objects.model._meta.db_table
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

        # Prepare vendor inserts
        df_vendor = pd.read_csv(metadata.vendor_data_path)
        df_vendor = df_vendor.where(pd.notnull(df_vendor), None)

        vendor_insert_stm = get_insert_values_into_table_stm(self.VENDOR_TABLE,
                                                             ['id', 'nif_id', 'vendor'],
                                                             len(df_vendor))

        # Prepare vendor domain inserts
        df_vendor_domain = pd.read_csv(metadata.vendor_domain_data_path)
        df_vendor_domain = df_vendor_domain.where(pd.notnull(df_vendor_domain), None)

        vendor_domain_insert_stm = get_insert_values_into_table_stm(self.VENDOR_DOMAIN_TABLE,
                                                                    ['id', 'domain_name', 'vendor_id', 'status',
                                                                     'link'],
                                                                    len(df_vendor_domain))

        # Prepare raw antibody inserts

        transaction_start = timer()
        logging.info("Ingestion process started")

        with transaction.atomic():
            with connection.cursor() as cursor:

                # delete tables content (opposite order of insertion)
                tables_to_delete = [self.SPECIE_TABLE, self.ANTIBODY_TABLE,
                                    self.ANTIGEN_TABLE, self.VENDOR_SYNONYM_TABLE,
                                    self.VENDOR_DOMAIN_TABLE, self.VENDOR_TABLE]
                start = timer()

                for ttd in tables_to_delete:
                    cursor.execute(TRUNCATE_STM.format(table_name=ttd))

                end = timer()
                logging.info(f"Tables truncated ({end - start} seconds)")

                # insert vendors
                vendor_synonyms_params = []
                vendor_params = []
                start = timer()

                for index, row in df_vendor.iterrows():
                    vendor_params.extend(
                        [row['id'], row['nifID'], row['vendor']])
                    synonyms_str = row['synonym']
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

                end = timer()
                logging.info(f"Vendors added ({end - start} seconds)")

                # insert vendors domains
                vendor_domain_params = []
                start = timer()

                for index, row in df_vendor_domain.iterrows():
                    vendor_domain_params.extend(
                        [row['id'], row['domain_name'], row['vendor_id'],
                         row['status'].upper(), False])
                cursor.execute(vendor_domain_insert_stm, vendor_domain_params)

                end = timer()
                logging.info(f"Vendor domains added ({end - start} seconds)")

                # Create copy table
                start = timer()

                cursor.execute(get_create_table_stm(self.TMP_TABLE, ANTIBODY_HEADER))

                # Insert raw data into tmp table

                d_types = ANTIBODY_HEADER.copy()
                for dt in d_types:
                    if dt == 'int':
                        d_types[dt] = 'int64'
                    else:
                        d_types[dt] = 'unicode'

                for antibody_data_path in metadata.antibody_data_paths:
                    logging.info(antibody_data_path)
                    len_csv = sum(1 for _ in open(antibody_data_path, 'r'))
                    for i, chunk in enumerate(pd.read_csv(antibody_data_path, chunksize=CHUNK_SIZE, dtype=d_types)):
                        chunk = chunk.where(pd.notnull(chunk), None)

                        raw_data_insert_stm = get_insert_values_into_table_stm(self.TMP_TABLE, ANTIBODY_HEADER.keys(),
                                                                               len(chunk))
                        cursor.execute(raw_data_insert_stm, chunk.to_numpy().flatten().tolist())
                        logging.info(f"File progress: {int(min((i + 1) * CHUNK_SIZE, len_csv) / len_csv * 100)}% ")

                end = timer()
                logging.info(f"Temporary table filled ({end - start} seconds)")

                # Insert select distinct antigen
                start = timer()

                cursor.execute(get_insert_into_table_select_stm(self.ANTIGEN_TABLE,
                                                                'ab_target',
                                                                True,
                                                                'ab_target',
                                                                self.TMP_TABLE))

                # Update antigen with ids
                antigen_update_stm = f"UPDATE {self.ANTIGEN_TABLE} " \
                                     f"SET ab_target_entrez_gid=TMP.ab_target_entrez_gid, " \
                                     f"uniprot_id=TMP.uniprot_id " \
                                     f"FROM {self.TMP_TABLE} as TMP " \
                                     f"WHERE {self.ANTIGEN_TABLE}.ab_target=TMP.ab_target; "
                cursor.execute(antigen_update_stm)

                end = timer()
                logging.info(f"Genes added ({end - start} seconds)")

                # Insert into species

                get_species_stm = f"SELECT DISTINCT target_species FROM {self.TMP_TABLE} " \
                                  f"UNION " \
                                  f"SELECT DISTINCT source_organism FROM {self.TMP_TABLE}"

                start = timer()

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

                end = timer()
                logging.info(f"Species added ({end - start} seconds)")

                # Insert into antibody

                antibody_stm = f"INSERT INTO {self.ANTIBODY_TABLE} (ix, ab_name, ab_id, accession, commercial_type, uid, catalog_num, cat_alt, " \
                               f"vendor_id, url, antigen_id, target_subregion, target_modification, " \
                               f"epitope, clonality, clone_id, product_isotype, " \
                               f"product_conjugate, defining_citation, product_form, comments, feedback, " \
                               f"curator_comment, disc_date, status, insert_time, curate_time, source_organism_id)" \
                               f"SELECT DISTINCT ix, ab_name, ab_id, ab_id_old, commercial_type, " \
                               f"uid, catalog_num, cat_alt, vendor_id, url, antigen.id, " \
                               f"target_subregion, target_modification, epitope, clonality, " \
                               f"clone_id, product_isotype, product_conjugate, defining_citation, product_form, " \
                               f"comments, feedback, curator_comment, disc_date, status, " \
                               f"to_timestamp(cast(insert_time as BIGINT) / 1000000.0), " \
                               f"to_timestamp(cast(curate_time as BIGINT) / 1000000.0), SP.id " \
                               f"FROM {self.TMP_TABLE} as TMP " \
                               f"LEFT JOIN {self.VENDOR_TABLE} as vendor " \
                               f"ON TMP.vendor_id = vendor.id " \
                               f"LEFT JOIN {self.ANTIGEN_TABLE} as antigen " \
                               f"ON TMP.ab_target = antigen.ab_target " \
                               f"LEFT JOIN {self.SPECIE_TABLE} as SP " \
                               f"ON TMP.source_organism = SP.name "

                start = timer()

                cursor.execute(antibody_stm)

                end = timer()

                logging.info(f"Antibodies added ({end - start} seconds)")

                # Insert into antibody species
                start = timer()

                for antibody_data_path in metadata.antibody_data_paths:
                    for chunk in pd.read_csv(antibody_data_path, chunksize=CHUNK_SIZE, dtype=d_types):
                        chunk = chunk.where(pd.notnull(chunk), None)

                        species_params = []
                        for index, row in chunk.iterrows():
                            target_species = row['target_species']
                            if target_species:
                                for specie in row['target_species'].split(';'):
                                    clean_specie = get_clean_species_str(specie)
                                    species_params.extend([row['ix'], species_map[clean_specie]])

                antibody_species_insert_stm = get_insert_values_into_table_stm(
                    AntibodySpecies.objects.model._meta.db_table, ['antibody_id', 'specie_id'],
                    int(len(species_params) / 2))

                cursor.execute(antibody_species_insert_stm, species_params)

                end = timer()
                logging.info(f"AntibodySpecies added ({end - start} seconds)")

                # Update vendor domain link
                antigen_update_stm = f"UPDATE {self.VENDOR_DOMAIN_TABLE} " \
                                     f"SET link = True " \
                                     f"FROM {self.TMP_TABLE} " \
                                     f"WHERE {self.VENDOR_DOMAIN_TABLE}.vendor_id={self.TMP_TABLE}.vendor_id " \
                                     f"AND {self.TMP_TABLE}.link = 'yes'; "
                start = timer()

                cursor.execute(antigen_update_stm)

                end = timer()

                logging.info(f"Vendor domain links updated ({end - start} seconds)")

                # Reset sequence fields
                tables_to_restart_seq = {
                    'api_antibody_ix_seq': ANTIBODY_ANTIBODY_START_SEQ,
                    'api_vendor_id_seq': ANTIBODY_VENDOR_START_SEQ,
                    'api_vendordomain_id_seq': ANTIBODY_VENDOR_DOMAIN_START_SEQ,
                }

                start = timer()

                for ttr in tables_to_restart_seq:
                    cursor.execute(get_restart_seq_stm(ttr, tables_to_restart_seq[ttr]))

                reset_sequence_sql = connection.ops.sequence_reset_sql(no_style(),
                                                                       [Specie, Gene, AntibodySpecies, VendorSynonym])
                for rss in reset_sequence_sql:
                    cursor.execute(rss)

                end = timer()
                logging.info(f"Sequence tables updated ({end - start} seconds)")

                # Drop tmp table
                start = timer()

                cursor.execute(DROP_TABLE_STM.format(table_name=self.TMP_TABLE))

                end = timer()
                logging.info(f"Temporary table dropped ({end - start} seconds)")

        transaction_end = timer()
        logging.info(f"Ingestion finished in {transaction_end - transaction_start} seconds")
