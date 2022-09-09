from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Ingests antibody data into the database"

    def add_arguments(self, parser):
        parser.add_argument("antibody_table_uri", type=str)
        parser.add_argument("vendor_table_uri", type=str)
        parser.add_argument("vendor_domain_table_uri", type=str)

    def handle(self, *args, **options):
        print(options["antibody_table"])
        pass
