from django.test import TestCase
from api.repositories.filters_repository import (
    check_filters_are_valid,
    convert_filters_to_q,
)
from .data.test_data import (
    INCOMPLETE_TEST_FILTER_AND_SEARCH_REQUEST_BODY,
    COMPLETE_TEST_FILTER_AND_SEARCH_REQUEST_BODY,
)
from .data.test_data import example_ab2, example_ab
from api.services.antibody_service import create_antibody
from api.repositories.search_repository import fts_and_filter_antibodies
from api.models import STATUS

from openapi.models import AddAntibody as AddAntibodyDTO
from openapi.models import (
    Operation,
    Sortorder,
    KeyValueSortOrderPair,
    KeyValuePair,
    KeyValueArrayPair,
)
from cloudharness.middleware import set_authentication_token, get_authentication_token
from api.services.user_service import get_current_user_id

token = "eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICJJUHJQcnZBanBrZ19HQlVUSVN5YVBoaXRMeUtVNDlQUGJRUTlPaWNBWEtzIn0.eyJleHAiOjE3MTAyMzg2MDAsImlhdCI6MTcxMDIyNzgwMCwiYXV0aF90aW1lIjoxNzEwMjI3ODAwLCJqdGkiOiIxZTFkMjRmMy0zMTU3LTRhNzEtOGI4Ny0yNzZhZjBkMGFjMTUiLCJpc3MiOiJodHRwczovL2FjY291bnRzLmFyZWcuZGV2Lm1ldGFjZWxsLnVzL2F1dGgvcmVhbG1zL2FyZWciLCJhdWQiOlsid2ViLWNsaWVudCIsImFjY291bnQiXSwic3ViIjoiNjZhOWRkNTQtMjIxNC00ZWQ3LWI0ZjgtZGFhNWJmM2M5YTc5IiwidHlwIjoiQmVhcmVyIiwiYXpwIjoid2ViLWNsaWVudCIsInNlc3Npb25fc3RhdGUiOiI1MzMyNDQ5MS0zNmY4LTRlODctOGE5YS0yZTIyODc3YmQxMDciLCJhY3IiOiIxIiwiYWxsb3dlZC1vcmlnaW5zIjpbIioiXSwicmVhbG1fYWNjZXNzIjp7InJvbGVzIjpbImFkbWluaXN0cmF0b3IiLCJkZWZhdWx0LXJvbGVzLWFyZWciXX0sInJlc291cmNlX2FjY2VzcyI6eyJhY2NvdW50Ijp7InJvbGVzIjpbIm1hbmFnZS1hY2NvdW50IiwibWFuYWdlLWFjY291bnQtbGlua3MiLCJ2aWV3LXByb2ZpbGUiXX19LCJzY29wZSI6Im9wZW5pZCBwcm9maWxlIGFkbWluaXN0cmF0b3Itc2NvcGUgZW1haWwiLCJzaWQiOiI1MzMyNDQ5MS0zNmY4LTRlODctOGE5YS0yZTIyODc3YmQxMDciLCJlbWFpbF92ZXJpZmllZCI6ZmFsc2UsIm5hbWUiOiJGaWxpcHBvIExlZGRhIiwicHJlZmVycmVkX3VzZXJuYW1lIjoiYSIsImdpdmVuX25hbWUiOiJGaWxpcHBvIiwiZmFtaWx5X25hbWUiOiJMZWRkYSIsImVtYWlsIjoiYUBhYS5pdCJ9.RShiiCZPEwz2IxEQqU2TBB1F6NQIOMfcrVU99eMSlXEahb38VegqUyIqUfoQUrQAHqnyysR67HeBuCq2SNh9ctxpAiEpFq7LAkqpEIQfByvdyDsBArT0jeWd6DuQ91_7PAdSPWqFEr-uFo9476NQZecrIuXCaNC3rrHbPb6GZKwT6gUMu_sCYAawT8jA_V9rpfgedM5PuqJHTp40of-ZDchD7Cc2NTIE2RopgkKifxtRRjQ9wwudz0hxKjVb9E9GCtkaA-MjDdEeVxnSgTu2p8Y9EaPOoZKt-zt0XTjRT8otwx7yOzz1euhDVh1-1zBb7V3Lt-w4BW19draYkGWMzg"


class SearchAndFilterAntibodiesTestCase(TestCase):
    def setUp(self):
        if token:
            set_authentication_token(token)

    def test_check_filters_are_valid(self):
        # Test empty filters
        self.assertFalse(check_filters_are_valid({}))

        self.assertFalse(
            check_filters_are_valid(INCOMPLETE_TEST_FILTER_AND_SEARCH_REQUEST_BODY)
        )  ## Will be false since three fields are missing

        # add the ones that are missing
        INCOMPLETE_TEST_FILTER_AND_SEARCH_REQUEST_BODY.isEmpty = []
        INCOMPLETE_TEST_FILTER_AND_SEARCH_REQUEST_BODY.operation = Operation.and_
        INCOMPLETE_TEST_FILTER_AND_SEARCH_REQUEST_BODY.isUserScope = True
        self.assertTrue(
            check_filters_are_valid(INCOMPLETE_TEST_FILTER_AND_SEARCH_REQUEST_BODY)
        )

        # Test invalid filter type - not of the format FilterRequest
        invalid_field = {"notTheField": []}
        self.assertFalse(check_filters_are_valid(invalid_field))

        # test invalid key
        valid_key_validation = INCOMPLETE_TEST_FILTER_AND_SEARCH_REQUEST_BODY.copy()
        valid_key_validation.contains[0].key = "notAField"
        self.assertFalse(check_filters_are_valid(valid_key_validation))

        # remove sortOn and check if false
        valid_key_validation.sortOn = None
        self.assertFalse(check_filters_are_valid(valid_key_validation))

        # if setting sortOn is [] and key is valid
        valid_key_validation.sortOn = []
        valid_key_validation.contains[0].key = "ab_name"
        self.assertTrue(check_filters_are_valid(valid_key_validation))

    def test_search_and_filter_antibodies(self):
        # FOR Search alone - catalog number
        ab = create_antibody(AddAntibodyDTO(**example_ab), "aaaa")
        ab2 = create_antibody(AddAntibodyDTO(**example_ab2), "aaaa")
        from api.models import Antibody

        all_antibodies = Antibody.objects.all()
        self.assertEqual(len(all_antibodies), 2)

        for an in all_antibodies:
            an.status = STATUS.CURATED
            an.save()

        # convert them to curated
        antibodies = fts_and_filter_antibodies(
            1, 10, "N176A", COMPLETE_TEST_FILTER_AND_SEARCH_REQUEST_BODY
        )
        # Check the count - antibodies[1] and items - antibodies[0]
        self.assertEqual(antibodies[1], 1)
        self.assertEqual(antibodies[0][0].catalogNum, example_ab["catalogNum"])
        self.assertEqual(antibodies[0][0].abName, example_ab["abName"])

        # ONLY SORTING
        filter_fts_sort = COMPLETE_TEST_FILTER_AND_SEARCH_REQUEST_BODY
        sortpair = KeyValueSortOrderPair(key="catalog_num", value=Sortorder.asc)
        filter_fts_sort.sortOn.append(sortpair)
        antibodies = fts_and_filter_antibodies(1, 10, "", filter_fts_sort)
        self.assertEqual(antibodies[1], 2)

        # If you check the test data - example_ab.catalogNum is N176A/35
        # and example_ab2.catalogNum is ENCAB558DXQ, hence the order check
        self.assertEqual(antibodies[0][0].catalogNum, example_ab2["catalogNum"])
        self.assertEqual(antibodies[0][1].catalogNum, example_ab["catalogNum"])

        # FILTERING WITH SORTING - No search
        # filter_fts_sort.contains[0].key = "catalogNum"
        # filter_fts_sort.contains[0].value = "N176A/35"
        contains_map = KeyValuePair(key="catalog_num", value="N176A/35")
        filter_fts_sort.contains.append(contains_map)
        antibodies = fts_and_filter_antibodies(1, 10, "", filter_fts_sort)
        self.assertEqual(antibodies[1], 1)
        self.assertEqual(antibodies[0][0].catalogNum, example_ab["catalogNum"])

        # FILTERING WITH SORTING - search
        antibodies = fts_and_filter_antibodies(1, 10, "DXQ", filter_fts_sort)
        self.assertEqual(antibodies[1], 0)

        # CHECK ISANY - and foreign key - vendor
        # Should return only one
        filter_fts_sort.sortOn[0].key = "vendor"
        filter_fts_sort.sortOn[0].sortorder = Sortorder.asc
        filter_fts_sort.contains = []
        filter_fts_sort.isAnyOf = [
            KeyValueArrayPair(key="vendor", value=["Andrew Dingwall", "John Doe"])
        ]
        antibodies = fts_and_filter_antibodies(1, 10, "", filter_fts_sort)
        self.assertEqual(antibodies[1], 1)
        self.assertEqual(antibodies[0][0].catalogNum, example_ab2["catalogNum"])

        # should return two
        filter_fts_sort.isAnyOf = [
            KeyValueArrayPair(key="vendor", value=["Andrew Dingwall", "My vendorname"])
        ]
        antibodies = fts_and_filter_antibodies(1, 10, "", filter_fts_sort)
        self.assertEqual(antibodies[1], 2)
        self.assertEqual(
            antibodies[0][0].catalogNum, example_ab2["catalogNum"]
        )  ## this is first because Andrew Dingwall comes first
        self.assertEqual(antibodies[0][1].catalogNum, example_ab["catalogNum"])

        filter_fts_sort.sortOn[0].sortorder = Sortorder.desc
        filter_fts_sort.sortOn[0].key = "species"
        filter_fts_sort.isAnyOf = []
        antibodies = fts_and_filter_antibodies(1, 10, "", filter_fts_sort)
        self.assertEqual(antibodies[1], 2)
        self.assertEqual(antibodies[0][0].catalogNum, example_ab2["catalogNum"])

        # Check isEmpty and isNotEmpty
        example_ab3 = example_ab.copy()
        example_ab3["catalogNum"] = None
        ab3 = create_antibody(AddAntibodyDTO(**example_ab3), "aaaa")
        all_antibodies = Antibody.objects.all()
        for an in all_antibodies:
            an.status = STATUS.CURATED
            an.save()

        filter_fts_sort.isEmpty = ["catalog_num"]
        filter_fts_sort.sortOn = []
        antibodies = fts_and_filter_antibodies(1, 10, "", filter_fts_sort)
        self.assertEqual(antibodies[1], 1)
        self.assertEqual(antibodies[0][0].catalogNum, example_ab3["catalogNum"])

        filter_fts_sort.isEmpty = []
        filter_fts_sort.isNotEmpty = ["catalog_num"]
        antibodies = fts_and_filter_antibodies(1, 10, "", filter_fts_sort)
        self.assertEqual(antibodies[1], 2)
