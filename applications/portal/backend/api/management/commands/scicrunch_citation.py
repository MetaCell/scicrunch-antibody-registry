"""
This File is to get the citation metric from the 
scricrunch API - https://api.scicrunch.io/elastic/v1/RIN_Tool_pr/_search?q=AB_90755&key={SCICRUNCH_API_KEY}

"""

from api.models import Antibody, STATUS
from django.core.management.base import BaseCommand
from cloudharness.utils.secrets import get_secret
from api.services.antibody_service import get_curated_antibodies_ids
from api.services.ingest_service import fetch_scicrunch_citation_metric, RateLimiter, set_citation_metric
from api.utilities.exceptions import FetchCitationMetricFailed
import sys
import os
import logging

scicrunch_api_key = os.getenv("SCICRUNCH_API_SECRET", get_secret("scicrunch-api-key")).strip()


class Command(BaseCommand):
    help = "Ingests citation metric from scicrunch"

    def add_arguments(self, parser):
        parser.add_argument('--max_requests_per_second', type=int, default=10)

    def log_error(self, error):
        logging.exception(error)

    def log(self, msg):
        logging.info(msg)

    def handle(self, *args, **options):
        requests_per_second_limit = options.get('max_requests_per_second', 10)
        
        antibodies_ids = get_curated_antibodies_ids()

        api_request_rate_limiter = RateLimiter(
            max_requests_per_second=requests_per_second_limit)
        total_anticipated_requests = len(antibodies_ids)
        failed_antibody_ids = []

        for ab_id in antibodies_ids:
            try:
                self.log(f"Processing Antibody: {ab_id}")
                self.process_antibody_ingestion(ab_id)
            except FetchCitationMetricFailed as e:
                self.log_error(e)
                failed_antibody_ids.append(ab_id)
            except Exception as e:
                self.log_error(e)
                failed_antibody_ids.append(ab_id)
            if self.has_too_many_failures(failed_antibody_ids, total_anticipated_requests):
                break
            api_request_rate_limiter.add_request()

        self.log_failed_antibodies(failed_antibody_ids)

    def process_antibody_ingestion(self, ab_id):

        number_of_citations = fetch_scicrunch_citation_metric(
            ab_id, scicrunch_api_key
        )
        if number_of_citations is not None:
            ingested = set_citation_metric(
                ab_id, number_of_citations)

        

    def log_failed_antibodies(self, failed_antibody_ids):
        if failed_antibody_ids:
            antibodies_failed = (
                ", ".join(failed_antibody_ids)
                if len(failed_antibody_ids) < 10
                else ", ".join(failed_antibody_ids[:10]) + "..."
            )
            self.log_error(
                f"Failed for Antibodies: {antibodies_failed}. Exiting the script"
            )
            self.log_error(f"Total Failed: {len(failed_antibody_ids)}")
            sys.exit(1)

    def has_too_many_failures(self, failed_antibody_ids, total_anticipated_requests):
        # if more than 1% of the total fails then stop the script
        if len(failed_antibody_ids) / total_anticipated_requests > 0.1:
            self.log_error(
                "More than 1% of the requests failed. Exiting the script"
            )
            return True
        return False
