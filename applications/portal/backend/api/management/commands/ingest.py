import logging
from timeit import default_timer as timer

from django.core.management.base import BaseCommand
from django.db import transaction, connection

from api.management.ingestion.ingestor import Ingestor
from api.management.ingestion.preprocessor import Preprocessor


class Command(BaseCommand):
    help = "Ingests antibody data into the database"

    def add_arguments(self, parser):
        parser.add_argument("file_id", type=str)

    def handle(self, *args, **options):
        metadata = Preprocessor(options["file_id"]).preprocess()

        transaction_start = timer()
        logging.info("Ingestion process started")

        with transaction.atomic():
            with connection.cursor() as cursor:
                Ingestor(metadata, cursor).ingest()

        transaction_end = timer()
        logging.info(f"Ingestion finished in {transaction_end - transaction_start} seconds")
