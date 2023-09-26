import logging
from timeit import default_timer as timer
from urllib.parse import urlparse
from urllib.parse import parse_qs

from django.core.management.base import BaseCommand
from django.db import transaction, connection

from api.management.ingestion.ingestor import Ingestor
from api.management.ingestion.preprocessor import Preprocessor


def parse_drive_link(drive_link_or_id: str):
    if "http" not in drive_link_or_id:
        return drive_link_or_id
    else:
        try:
            # https://drive.google.com/open?id=FILE_ID&usp=drive_fs
            return parse_qs(urlparse(drive_link_or_id).query)['id'][0]
        except:
            # https://drive.google.com/file/d/FILE_ID/view?usp=drive_link
            return drive_link_or_id.split("/")[-2]
        
class Command(BaseCommand):
    help = "Ingests antibody data into the database"

    def add_arguments(self, parser):
        parser.add_argument("file_id", type=str)
        parser.add_argument("--hot", action="store_true",
            help="execute a hot load (no replacements)",)

    def handle(self, *args, **options):
        metadata = Preprocessor(parse_drive_link(options["file_id"])).preprocess()

        transaction_start = timer()
        logging.info("Ingestion process started")

        self.ingest(metadata, options["hot"])

        transaction_end = timer()
        logging.info(f"Ingestion finished in {transaction_end - transaction_start} seconds")

    def ingest(self, metadata, hot=False):
        with transaction.atomic():
            Ingestor(metadata, connection, hot).ingest()
