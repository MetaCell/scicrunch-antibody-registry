from django.test import TestCase
from .data.test_data import (
    COMPLETE_TEST_FILTER_AND_SEARCH_REQUEST_BODY,
)
from .data.test_data import example_ab2, example_ab
from api.services.antibody_service import create_antibody
from api.repositories.filter_repository import plain_filter_antibodies

from openapi.models import AddAntibody as AddAntibodyDTO, KeyValuePair, KeyValueSortOrderPair, Sortorder
from cloudharness.middleware import set_authentication_token

token = "eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICJJUHJQcnZBanBrZ19HQlVUSVN5YVBoaXRMeUtVNDlQUGJRUTlPaWNBWEtzIn0.eyJleHAiOjE3MTAyMzg2MDAsImlhdCI6MTcxMDIyNzgwMCwiYXV0aF90aW1lIjoxNzEwMjI3ODAwLCJqdGkiOiIxZTFkMjRmMy0zMTU3LTRhNzEtOGI4Ny0yNzZhZjBkMGFjMTUiLCJpc3MiOiJodHRwczovL2FjY291bnRzLmFyZWcuZGV2Lm1ldGFjZWxsLnVzL2F1dGgvcmVhbG1zL2FyZWciLCJhdWQiOlsid2ViLWNsaWVudCIsImFjY291bnQiXSwic3ViIjoiNjZhOWRkNTQtMjIxNC00ZWQ3LWI0ZjgtZGFhNWJmM2M5YTc5IiwidHlwIjoiQmVhcmVyIiwiYXpwIjoid2ViLWNsaWVudCIsInNlc3Npb25fc3RhdGUiOiI1MzMyNDQ5MS0zNmY4LTRlODctOGE5YS0yZTIyODc3YmQxMDciLCJhY3IiOiIxIiwiYWxsb3dlZC1vcmlnaW5zIjpbIioiXSwicmVhbG1fYWNjZXNzIjp7InJvbGVzIjpbImFkbWluaXN0cmF0b3IiLCJkZWZhdWx0LXJvbGVzLWFyZWciXX0sInJlc291cmNlX2FjY2VzcyI6eyJhY2NvdW50Ijp7InJvbGVzIjpbIm1hbmFnZS1hY2NvdW50IiwibWFuYWdlLWFjY291bnQtbGlua3MiLCJ2aWV3LXByb2ZpbGUiXX19LCJzY29wZSI6Im9wZW5pZCBwcm9maWxlIGFkbWluaXN0cmF0b3Itc2NvcGUgZW1haWwiLCJzaWQiOiI1MzMyNDQ5MS0zNmY4LTRlODctOGE5YS0yZTIyODc3YmQxMDciLCJlbWFpbF92ZXJpZmllZCI6ZmFsc2UsIm5hbWUiOiJGaWxpcHBvIExlZGRhIiwicHJlZmVycmVkX3VzZXJuYW1lIjoiYSIsImdpdmVuX25hbWUiOiJGaWxpcHBvIiwiZmFtaWx5X25hbWUiOiJMZWRkYSIsImVtYWlsIjoiYUBhYS5pdCJ9.RShiiCZPEwz2IxEQqU2TBB1F6NQIOMfcrVU99eMSlXEahb38VegqUyIqUfoQUrQAHqnyysR67HeBuCq2SNh9ctxpAiEpFq7LAkqpEIQfByvdyDsBArT0jeWd6DuQ91_7PAdSPWqFEr-uFo9476NQZecrIuXCaNC3rrHbPb6GZKwT6gUMu_sCYAawT8jA_V9rpfgedM5PuqJHTp40of-ZDchD7Cc2NTIE2RopgkKifxtRRjQ9wwudz0hxKjVb9E9GCtkaA-MjDdEeVxnSgTu2p8Y9EaPOoZKt-zt0XTjRT8otwx7yOzz1euhDVh1-1zBb7V3Lt-w4BW19draYkGWMzg"


class PlainFilterAntibodiesTestCase(TestCase):
    def setUp(self):
        if token:
            set_authentication_token(token)

    def test_plain_filter_antibodies(self):
        ab = create_antibody(AddAntibodyDTO(**example_ab), "66a9dd54-2214-4ed7-b4f8-daa5bf3c9a79")
        ab2 = create_antibody(AddAntibodyDTO(**example_ab2), "66a9dd54-2214-4ed7-b4f8-daa5bf3c9a79")
        example_ab3 = example_ab2.copy()
        example_ab3["catalogNum"] = "FOX176A/35"
        example_ab3["vendorName"] = "FOX"

        ab3 = create_antibody(AddAntibodyDTO(**example_ab3), "66a9dd54-2214-4ed7-b4f8-daa5bf3c9a79")

        COMPLETE_TEST_FILTER_AND_SEARCH_REQUEST_BODY.isUserScope = True
        COMPLETE_TEST_FILTER_AND_SEARCH_REQUEST_BODY.isNotEmpty = []

        antibodies, count = plain_filter_antibodies(1, 10, COMPLETE_TEST_FILTER_AND_SEARCH_REQUEST_BODY)
        self.assertEqual(count, 3)
        self.assertEqual(antibodies[0].catalogNum, example_ab3["catalogNum"])  # since plain sorting by default "-ix"
        self.assertEqual(antibodies[1].catalogNum, example_ab2["catalogNum"])
        self.assertEqual(antibodies[0].vendorName, example_ab3["vendorName"])

        # FILTERING WITHOUT SORTING
        filter_sort = COMPLETE_TEST_FILTER_AND_SEARCH_REQUEST_BODY

        filter_sort.contains.append(KeyValuePair(key="catalog_num", value="N176A/35"))
        antibodies, count = plain_filter_antibodies(1, 10, filter_sort)
        self.assertEqual(count, 1)
        self.assertEqual(antibodies[0].catalogNum, example_ab["catalogNum"])

        filter_sort.contains = []
        filter_sort.sortOn = [KeyValueSortOrderPair(key="catalog_num", sortorder=Sortorder.asc)]
        antibodies, count = plain_filter_antibodies(1, 10, filter_sort)
        self.assertEqual(count, 3)

        # ab2 -> ab3 -> ab : ENCAB558DXQ -> FOX176A/35 -> N176A/35
        self.assertEqual(antibodies[0].vendorName, example_ab2["vendorName"])
        self.assertEqual(antibodies[1].catalogNum, example_ab3["catalogNum"])
        self.assertEqual(antibodies[2].catalogNum, example_ab["catalogNum"])
