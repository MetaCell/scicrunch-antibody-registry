import itertools
import logging
import string

import pandas as pd
from django.core.management.color import no_style
from django.db import connection

from cloudharness import log

from api.management.ingestion.preprocessor import AntibodyMetadata
from api.management.ingestion.users_ingestor import UsersIngestor
from api.models import Antibody, Gene, Vendor, VendorDomain, Specie, \
    VendorSynonym, AntibodySpecies
from api.utilities.decorators import timed_class_method
from portal.settings import ANTIBODY_ANTIBODY_START_SEQ, ANTIBODY_VENDOR_START_SEQ, \
    ANTIBODY_VENDOR_DOMAIN_START_SEQ, ANTIBODY_HEADER, D_TYPES, UID_INDEX
from portal.settings import CHUNK_SIZE

TRUNCATE_STM = "TRUNCATE TABLE {table_name} CASCADE;"
INSERT_INTO_VALUES_STM = "INSERT INTO {table_name} ({columns}) VALUES {} ;"
DROP_TABLE_STM = "DROP TABLE IF EXISTS {table_name} ;"
CREATE_TABLE_STM = "CREATE TABLE {table_name} ({columns}) ; "
INSERT_INTO_SELECT_STM = "INSERT INTO {to_table_name} ({to_columns}) SELECT {distinct} {from_columns} FROM {from_table_name};"
RESTART_SEQ_STM = "ALTER SEQUENCE {table_name} RESTART WITH {value};"


def get_restart_seq_stm(table_name, value):
    return RESTART_SEQ_STM.format(table_name=table_name, value=value)


def get_create_table_stm(table_name, columns_dict):
    columns_str = ", ".join(
        [f"{column} {columns_dict[column]}" for column in columns_dict])
    return CREATE_TABLE_STM.format(table_name=table_name, columns=columns_str)


def get_insert_into_table_select_stm(to_table_name, to_columns, distinct, from_columns, from_table_name):
    distinct_str = 'DISTINCT' if distinct else ''
    return INSERT_INTO_SELECT_STM.format(to_table_name=to_table_name, to_columns=to_columns, distinct=distinct_str,
                                         from_columns=from_columns, from_table_name=from_table_name)


def get_insert_values_into_table_stm(table_name, columns, entries):
    return INSERT_INTO_VALUES_STM.format(
        ', '.join(
            [f"({', '.join(['%s' for _ in range(0, len(columns))])})"] * entries),
        table_name=table_name,
        columns=', '.join(columns))


def get_clean_species_str(specie: str):
    return specie.translate(str.maketrans('', '', string.punctuation)).strip().lower()


class Ingestor:
    ANTIBODY_TABLE = Antibody.objects.model._meta.db_table
    ANTIGEN_TABLE = Gene.objects.model._meta.db_table
    SPECIE_TABLE = Specie.objects.model._meta.db_table
    VENDOR_DOMAIN_TABLE = VendorDomain.objects.model._meta.db_table
    VENDOR_SYNONYM_TABLE = VendorSynonym.objects.model._meta.db_table
    VENDOR_TABLE = Vendor.objects.model._meta.db_table
    TMP_TABLE = 'tmp_table'

    def __init__(self, metadata: AntibodyMetadata, cursor):
        self.metadata = metadata
        self.cursor = cursor
        try:
            self.users_ingestor = UsersIngestor(metadata.users_data_path)
        except Exception as e:
            log.error(f"Cannot ingest users: {str(e)}", exc_info=True)

    def ingest(self):
        species_map = {}

        # self._truncate_tables()
        # self._insert_vendors()
        # self._insert_vendor_domains()
        self._fill_tmp_table()
        # self._insert_genes()
        # self._insert_species(species_map)
        # self._insert_antibodies()
        # self._insert_antibody_species(species_map)
        # self._update_vendor_domains()
        # self._reset_auto_increment()
        self._drop_tmp_table()

    @timed_class_method('Tables truncated')
    def _truncate_tables(self):
        # delete tables content (opposite order of insertion)
        tables_to_delete = [self.SPECIE_TABLE, self.ANTIBODY_TABLE,
                            self.ANTIGEN_TABLE, self.VENDOR_SYNONYM_TABLE,
                            self.VENDOR_DOMAIN_TABLE, self.VENDOR_TABLE]

        for ttd in tables_to_delete:
            try:
                self.cursor.execute(TRUNCATE_STM.format(table_name=ttd))
            except:
                log.error("Cannot execute statement %s",
                          TRUNCATE_STM.format(table_name=ttd), exc_info=True)

    @timed_class_method('Vendors added ')
    def _insert_vendors(self):
        # Prepare vendor inserts
        df_vendor = pd.read_csv(self.metadata.vendor_data_path)
        df_vendor = df_vendor.where(pd.notnull(df_vendor), None)
        vendor_insert_stm = get_insert_values_into_table_stm(self.VENDOR_TABLE,
                                                             ['id', 'nif_id', 'vendor',
                                                                 'commercial_type'],
                                                             len(df_vendor))
        # insert vendors
        vendor_synonyms_params = []
        vendor_params = []
        for index, row in df_vendor.iterrows():
            vendor_params.extend(
                [row['id'], row['nifID'], row['vendor'], row['commercial_type']])
            synonyms_str = row['synonym']
            if synonyms_str:
                for s in synonyms_str.split(','):
                    vendor_synonyms_params.extend([row['id'], s])
        self.cursor.execute(vendor_insert_stm, vendor_params)

        # insert vendors synonyms
        vendor_synonyms_insert_stm = get_insert_values_into_table_stm(
            self.VENDOR_SYNONYM_TABLE,
            ['vendor_id', 'name'],
            int(len(vendor_synonyms_params) / 2))
        self.cursor.execute(vendor_synonyms_insert_stm, vendor_synonyms_params)

    @timed_class_method('Vendor domains added ')
    def _insert_vendor_domains(self):
        # Prepare vendor domains inserts
        df_vendor_domain = pd.read_csv(self.metadata.vendor_domain_data_path)
        df_vendor_domain = df_vendor_domain.where(
            pd.notnull(df_vendor_domain), None)

        vendor_domain_insert_stm = get_insert_values_into_table_stm(self.VENDOR_DOMAIN_TABLE,
                                                                    ['id', 'domain_name', 'vendor_id', 'status',
                                                                     'link'],
                                                                    len(df_vendor_domain))
        vendor_domain_params = []

        # insert vendor domains
        for index, row in df_vendor_domain.iterrows():
            vendor_domain_params.extend(
                [row['id'], row['domain_name'], row['vendor_id'],
                 row['status'].upper(), False])
        self.cursor.execute(vendor_domain_insert_stm, vendor_domain_params)

    @timed_class_method('Temporary table filled')
    def _fill_tmp_table(self):
        try:
            users_map = self.users_ingestor.get_users_map() if self.users_ingestor else {}
        except:
            log.error("Cannot ingest users", exc_info=True)
            users_map = {}
        self.cursor.execute(get_create_table_stm(
            self.TMP_TABLE, ANTIBODY_HEADER))

        # Insert raw data into tmp table
        for antibody_data_path in self.metadata.antibody_data_paths:
            logging.info(antibody_data_path)
            len_csv = sum(1 for _ in open(antibody_data_path, 'r'))
            for i, chunk in enumerate(pd.read_csv(antibody_data_path, chunksize=CHUNK_SIZE, dtype=D_TYPES)):
                chunk = chunk.where(pd.notnull(chunk), None)
                chunk['uid_legacy'] = chunk['uid']
                chunk['uid'] = chunk['uid_legacy'].apply(
                    lambda x: users_map.get(x, None))
                raw_data_insert_stm = get_insert_values_into_table_stm(self.TMP_TABLE, ANTIBODY_HEADER.keys(),
                                                                       len(chunk))

                self.cursor.execute(raw_data_insert_stm,
                                    chunk.to_numpy().flatten().tolist())
                logging.info(
                    f"File progress: {int(min((i + 1) * CHUNK_SIZE, len_csv) / len_csv * 100)}% ")

    @timed_class_method('Genes added')
    def _insert_genes(self):
        self.cursor.execute(get_insert_into_table_select_stm(self.ANTIGEN_TABLE,
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
        self.cursor.execute(antigen_update_stm)

    @timed_class_method('Species added')
    def _insert_species(self, species_map):
        get_species_stm = f"SELECT DISTINCT target_species FROM {self.TMP_TABLE} " \
                          f"UNION " \
                          f"SELECT DISTINCT source_organism FROM {self.TMP_TABLE}"
        self.cursor.execute(get_species_stm)
        species_id = 1
        for row in self.cursor:
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
        if len(species_map) > 0:
            self.cursor.execute(species_insert_stm, list(
                itertools.chain.from_iterable(species_map.items())))

    @timed_class_method('Antibodies added')
    def _insert_antibodies(self):

        antibody_stm = f"INSERT INTO {self.ANTIBODY_TABLE} (ix, ab_name, ab_id, accession, commercial_type, uid, catalog_num, cat_alt, " \
                       f"vendor_id, url, antigen_id, target_subregion, target_modification, " \
                       f"epitope, clonality, clone_id, product_isotype, " \
                       f"product_conjugate, defining_citation, product_form, comments, feedback, " \
                       f"curator_comment, disc_date, status, insert_time, curate_time, source_organism_id)" \
                       f"SELECT DISTINCT ix, ab_name, ab_id, ab_id_old, TMP.commercial_type, " \
                       f"uid, catalog_num, cat_alt, vendor_id, url, antigen.id, " \
                       f"target_subregion, target_modification, epitope, clonality, " \
                       f"clone_id, product_isotype, product_conjugate, defining_citation, product_form, " \
                       f"comments, feedback, curator_comment, disc_date, status, " \
                       f"to_timestamp(cast(insert_time as BIGINT)), " \
                       f"to_timestamp(cast(curate_time as BIGINT)), SP.id " \
                       f"FROM {self.TMP_TABLE} as TMP " \
                       f"LEFT JOIN {self.VENDOR_TABLE} as vendor " \
                       f"ON TMP.vendor_id = vendor.id " \
                       f"LEFT JOIN {self.ANTIGEN_TABLE} as antigen " \
                       f"ON TMP.ab_target = antigen.ab_target " \
                       f"LEFT JOIN {self.SPECIE_TABLE} as SP " \
                       f"ON TMP.source_organism = SP.name "

        self.cursor.execute(antibody_stm)

    @timed_class_method('AntibodySpecies added')
    def _insert_antibody_species(self, species_map):
        for antibody_data_path in self.metadata.antibody_data_paths:
            for chunk in pd.read_csv(antibody_data_path, chunksize=CHUNK_SIZE, dtype=D_TYPES):
                chunk = chunk.where(pd.notnull(chunk), None)

                species_params = []
                for index, row in chunk.iterrows():
                    target_species = row['target_species']
                    if target_species:
                        for specie in row['target_species'].split(';'):
                            clean_specie = get_clean_species_str(specie)
                            species_params.extend(
                                [row['ix'], species_map[clean_specie]])

                antibody_species_insert_stm = get_insert_values_into_table_stm(
                    AntibodySpecies.objects.model._meta.db_table, [
                        'antibody_id', 'specie_id'],
                    int(len(species_params) / 2))

                self.cursor.execute(
                    antibody_species_insert_stm, species_params)

    @timed_class_method('Vendor domain links updated')
    def _update_vendor_domains(self):
        vendor_domain_update_stm = f"UPDATE {self.VENDOR_DOMAIN_TABLE} " \
                                   f"SET link = True " \
                                   f"FROM {self.TMP_TABLE} " \
                                   f"WHERE {self.VENDOR_DOMAIN_TABLE}.vendor_id={self.TMP_TABLE}.vendor_id " \
                                   f"AND {self.TMP_TABLE}.link = 'yes'; "
        self.cursor.execute(vendor_domain_update_stm)

    @timed_class_method('Sequence tables updated')
    def _reset_auto_increment(self):
        tables_to_restart_seq = {
            'api_antibody_ix_seq': ANTIBODY_ANTIBODY_START_SEQ,
            'api_vendor_id_seq': ANTIBODY_VENDOR_START_SEQ,
            'api_vendordomain_id_seq': ANTIBODY_VENDOR_DOMAIN_START_SEQ,
        }

        for ttr in tables_to_restart_seq:
            self.cursor.execute(get_restart_seq_stm(
                ttr, tables_to_restart_seq[ttr]))

        reset_sequence_sql = connection.ops.sequence_reset_sql(no_style(),
                                                               [Specie, Gene, AntibodySpecies, VendorSynonym])
        for rss in reset_sequence_sql:
            self.cursor.execute(rss)

    @timed_class_method('Temporary table dropped')
    def _drop_tmp_table(self):
        self.cursor.execute(DROP_TABLE_STM.format(table_name=self.TMP_TABLE))
