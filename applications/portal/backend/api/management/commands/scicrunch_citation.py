"""
This File is to get the citation metric from the 
scricrunch API - https://api.scicrunch.io/elastic/v1/RIN_Tool_pr/_search?q=AB_90755&key={SCICRUNCH_API_KEY}

"""

from api.models import Antibody, STATUS
from django.core.management.base import BaseCommand
from cloudharness.utils.secrets import get_secret
from api.controllers.antibody_controller import get_curated_antibodies
from api.controllers.ingest_controller import ingest_scicrunch_citation_metric
from api.services.ingest_service import fetch_scicrunch_citation_metric, RateLimiter
from api.utilities.exceptions import FetchCitationMetricFailed
import sys
import logging

scicrunch_api_key = get_secret("scicrunch-api-key")


class Command(BaseCommand):
    help = "Ingests citation metric from scicrunch"

    def add_arguments(self, parser):
        parser.add_argument('--max_requests_per_second', type=int, default=10)


    def log_error(self, error):
        self.stdout.write(self.style.ERROR(error))

    def handle(self, *args, **options):
        requests_per_second_limit = options.get('max_requests_per_second', 10)
        antibodies_ids = self.get_curated_antibodies()

        api_request_rate_limiter = RateLimiter(max_requests_per_second=requests_per_second_limit)
        total_anticipated_requests = len(antibodies_ids)
        failed_antibody_ids = []
        for id in range(len(antibodies_ids)):
            self.process_antibody_ingestion(antibodies_ids, api_request_rate_limiter, failed_antibody_ids, id)
            if self.has_too_many_failures(failed_antibody_ids, total_anticipated_requests):
                break

        self.log_failed_antibodies(failed_antibody_ids)



    def process_antibody_ingestion(self, antibodies_ids, api_request_rate_limiter, failed_antibody_ids, id):
        ab_id = antibodies_ids[id]
        try:
            number_of_citations = fetch_scicrunch_citation_metric(
                ab_id, scicrunch_api_key
            )
            if number_of_citations is not None:
                ingested = ingest_scicrunch_citation_metric(ab_id, number_of_citations)
        except FetchCitationMetricFailed as e:
            self.log_error(e)
            failed_antibody_ids.append(ab_id)
        except Exception as e:
            self.log_error(e)
            failed_antibody_ids.append(ab_id)

        api_request_rate_limiter.add_request()


    def get_curated_antibodies(self):
        try:
            antibodies_ids = get_curated_antibodies()
        except Exception as e:
            self.log_error(f"{e}. Exiting the script")
            sys.exit(1)
        return antibodies_ids
    

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
        if len(failed_antibody_ids) / total_anticipated_requests > 0.01:
            self.log_error(
                "More than 1% of the requests failed. Exiting the script"
            )
            return True
        return False

