"""
This File is to get the citation metric from the 
scricrunch API - https://api.scicrunch.io/elastic/v1/RIN_Tool_pr/_search?q=AB_90755&key={SCICRUNCH_API_KEY}

"""

import requests
from api.models import Antibody, STATUS
from django.core.management.base import BaseCommand
from cloudharness.utils.secrets import get_secret

scicrunch_api_key = get_secret("SCICRUNCH_API_KEY")

def get_json_body(ab_id):
    return {
        "size": 3,
        "from": 0,
        "query": {
            "bool": {
                "should": [
                    {
                        "match_phrase": {
                            "resourceMentions.rrid.keyword": {"query": f"RRID:{ab_id}"}
                        }
                    },
                    {
                        "match_phrase": {
                            "rridMentions.rrid.keyword": {"query": f"RRID:{ab_id}"}
                        }
                    },
                    {
                        "match_phrase": {
                            "filteredMentions.rrid.keyword": {"query": f"RRID:{ab_id}"}
                        }
                    },
                ]
            }
        },
        "sort": [{"dc.publicationYear": {"order": "desc"}}, "_score"],
    }


class Command(BaseCommand):
    help = "Ingests citation metric from scicrunch"

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        antibodies_ids = Antibody.objects.filter(status=STATUS.CURATED).values_list(
            "ab_id", flat=True
        )
        citation_metrics = self.fetch_scicrunch_citation_metric(
            antibodies_ids, scicrunch_api_key
        )
        if citation_metrics:
            self.ingest_scicrunch_citation_metric(citation_metrics)
            self.stdout.write(
                self.style.SUCCESS(
                    f"Successfully fetched citation metric for all Antibodies"
                )
            )
        else:
            self.stdout.write(self.style.ERROR(f"Failed to ingest citation metrics"))


    def fetch_scicrunch_citation_metric(self, antibody_ids, scicrunch_api_key):
        citation_metrics = []
        # TODO: Add a rate limiter - The 10 requests per second (rps) baseline
        for ab_id in antibody_ids:
            abid = "AB_" + str(ab_id)
            # Below is the link to get the mentions
            # link_for_api = f"https://api.scicrunch.io/elastic/v1/RIN_Tool_pr/_search?q={abid}&key={scicrunch_api_key}"
            link_for_api = f"https://scicrunch.org/api/1/elastic/RIN_Mentions_pr/data/_search?key={scicrunch_api_key}"
            json_body = get_json_body(abid)
            try:
                response = requests.post(
                    link_for_api,
                    json=json_body,
                    headers={"Content-Type": "application/json"},
                )
                if response.status_code == 200:
                    res = response.json()
                    # Below is the old code to get the mentions
                    # citation_count = res["hits"]["hits"][0]["_source"]["mentions"][0][
                    #     "totalMentions"
                    # ]["count"]
                    citation_count = res["hits"]["total"]

                    citation_metrics.append({ab_id: citation_count})
                else:
                    self.stdout.write(
                        self.style.ERROR(f"Failed to fetch citation metrics")
                    )
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f"Failed to fetch citation metrics for {ab_id}")
                )
        return citation_metrics

    def ingest_scicrunch_citation_metric(self, citation_metrics):
        antibodies = []
        for citation in citation_metrics:
            try:
                for ab_id, citation_count in citation.items():
                    antibodies_filtered_by_id = Antibody.objects.filter(ab_id=ab_id)
                    for antibody in antibodies_filtered_by_id:
                        antibody.citation = citation_count
                        antibodies.append(antibody)
            except Antibody.DoesNotExist:
                self.stdout.write(
                    self.style.ERROR(f"Antibody with ab_id {ab_id} does not exist")
                )

        Antibody.objects.bulk_update(antibodies, ["citation"])
