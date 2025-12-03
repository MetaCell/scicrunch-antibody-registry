import requests
import time
import json
from portal.constants import CRONJOB_REQUEST_TEMPLATE
from api.utilities.exceptions import FetchCitationMetricFailed
from api.utilities.rate_limiter import RateLimiter
import logging
from api.models import Antibody, STATUS


def get_json_body(ab_id):
    json_request = json.dumps(
        CRONJOB_REQUEST_TEMPLATE).replace("{ab_id}", ab_id)
    return json.loads(json_request)


def fetch_scicrunch_citation_metric(antibody_id, scicrunch_api_key):
    abid = "AB_" + str(antibody_id)
    # Below is the link to get the mentions - GET request
    # link_for_api = f"https://api.scicrunch.io/elastic/v1/RIN_Tool_pr/_search?q={abid}&key={scicrunch_api_key}"

    # Below is the new POST request API to get the citations metrics
    link_for_api = f"https://scicrunch.org/api/1/elastic/RIN_Mentions_pr/data/_search?key={scicrunch_api_key}"
    json_body = get_json_body(abid)

    response = requests.post(
        link_for_api,
        json=json_body,
        headers={"Content-Type": "application/json"},
    )
    if response.status_code == 200:
        res = response.json()
        # Below is the old code to get the mentions for the GET request
        # citation_count = res["hits"]["hits"][0]["_source"]["mentions"][0][
        #     "totalMentions"
        # ]["count"]

        # Below is the new code to get the citations for the POST request
        return res["hits"]["total"]
    else:
        raise FetchCitationMetricFailed(abid)


def set_citation_metric(antibody_id, number_of_citation):

    antibodies_filtered_by_id = Antibody.objects.filter(ab_id=antibody_id)
    if not antibodies_filtered_by_id:
        raise Antibody.DoesNotExist
    for antibody in antibodies_filtered_by_id:
        antibody.citation = number_of_citation
        antibody.save(update_search=False)
    return antibodies_filtered_by_id
