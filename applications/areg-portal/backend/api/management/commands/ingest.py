import pandas as pd
from django.core.management.base import BaseCommand
from django.db import transaction, connection

from api.models import STATUS, CommercialType

TRUNCATE_STM = "TRUNCATE TABLE $tableName CASCADE;"
INSERT_INTO_STM = "INSERT INTO $tableName ($columns) VALUES {} ;"


def get_insert_into_table_stm(table_name, columns, entries):
    return INSERT_INTO_STM.replace('$tableName', table_name).replace('$columns', ', '.join(columns)).format(
        ', '.join([f"({', '.join(['%s' for _ in range(0, len(columns))])})"] * entries))


def clean_empty_value(value):
    if value == '(null)':
        return ''
    return value


def handle_undefined_commercial_type(value):
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

        # Prepare vendor inserts
        df_vendor = pd.read_csv(options['vendor_table_uri'])
        vendor_insert_stm = get_insert_into_table_stm('api_vendor',
                                                      ['id', 'nif_id', 'vendor', 'synonyms', 'commercial_type'],
                                                      len(df_vendor))

        # Prepare vendor domain inserts
        df_vendor_domain = pd.read_csv(options['vendor_domain_table_uri'])
        df_vendor_domain.drop_duplicates(subset=["domain_name"])
        vendor_domain_insert_stm = get_insert_into_table_stm('api_vendordomain',
                                                             ['id', 'domain_name', 'vendor_id', 'status'],
                                                             len(df_vendor_domain))

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
                # vendor_domain_params = []
                # for index, row in df_vendor_domain.iterrows():
                #     vendor_domain_params.extend(
                #         [row['id'], row['domain_name'], row['vendor_id'],
                #          status_reverse_map[row['status']]])
                # cursor.execute(vendor_domain_insert_stm, vendor_domain_params)

                print("Done")

                # Create copy table
                # Insert data
                # Insert select distinct antigen
                # Insert into antibody
                # (Be aware of the choices options)
