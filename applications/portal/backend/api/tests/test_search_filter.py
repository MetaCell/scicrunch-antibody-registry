from django.test import TestCase
from django.contrib.auth.models import User
from api.repositories.filtering_utils import check_filters_are_valid
from api.models import Antibody, STATUS
from api.schemas import (
    OperationEnum,
    SortOrderEnum,
    KeyValueSortOrderPair,
    KeyValuePair,
    KeyValueArrayPair,
    FilterRequest,
)
from api.api import api
from .data.test_data import example_ab2, example_ab
from .utils import LoggedinTestClient
from cloudharness.middleware import set_authentication_token
from cloudharness_django.models import Member

token = "eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICJJUHJQcnZBanBrZ19HQlVUSVN5YVBoaXRMeUtVNDlQUGJRUTlPaWNBWEtzIn0.eyJleHAiOjE3MTAyMzg2MDAsImlhdCI6MTcxMDIyNzgwMCwiYXV0aF90aW1lIjoxNzEwMjI3ODAwLCJqdGkiOiIxZTFkMjRmMy0zMTU3LTRhNzEtOGI4Ny0yNzZhZjBkMGFjMTUiLCJpc3MiOiJodHRwczovL2FjY291bnRzLmFyZWcuZGV2Lm1ldGFjZWxsLnVzL2F1dGgvcmVhbG1zL2FyZWciLCJhdWQiOlsid2ViLWNsaWVudCIsImFjY291bnQiXSwic3ViIjoiNjZhOWRkNTQtMjIxNC00ZWQ3LWI0ZjgtZGFhNWJmM2M5YTc5IiwidHlwIjoiQmVhcmVyIiwiYXpwIjoid2ViLWNsaWVudCIsInNlc3Npb25fc3RhdGUiOiI1MzMyNDQ5MS0zNmY4LTRlODctOGE5YS0yZTIyODc3YmQxMDciLCJhY3IiOiIxIiwiYWxsb3dlZC1vcmlnaW5zIjpbIioiXSwicmVhbG1fYWNjZXNzIjp7InJvbGVzIjpbImFkbWluaXN0cmF0b3IiLCJkZWZhdWx0LXJvbGVzLWFyZWciXX0sInJlc291cmNlX2FjY2VzcyI6eyJhY2NvdW50Ijp7InJvbGVzIjpbIm1hbmFnZS1hY2NvdW50IiwibWFuYWdlLWFjY291bnQtbGlua3MiLCJ2aWV3LXByb2ZpbGUiXX19LCJzY29wZSI6Im9wZW5pZCBwcm9maWxlIGFkbWluaXN0cmF0b3Itc2NvcGUgZW1haWwiLCJzaWQiOiI1MzMyNDQ5MS0zNmY4LTRlODctOGE5YS0yZTIyODc3YmQxMDciLCJlbWFpbF92ZXJpZmllZCI6ZmFsc2UsIm5hbWUiOiJGaWxpcHBvIExlZGRhIiwicHJlZmVycmVkX3VzZXJuYW1lIjoiYSIsImdpdmVuX25hbWUiOiJGaWxpcHBvIiwiZmFtaWx5X25hbWUiOiJMZWRkYSIsImVtYWlsIjoiYUBhYS5pdCJ9.RShiiCZPEwz2IxEQqU2TBB1F6NQIOMfcrVU99eMSlXEahb38VegqUyIqUfoQUrQAHqnyysR67HeBuCq2SNh9ctxpAiEpFq7LAkqpEIQfByvdyDsBArT0jeWd6DuQ91_7PAdSPWqFEr-uFo9476NQZecrIuXCaNC3rrHbPb6GZKwT6gUMu_sCYAawT8jA_V9rpfgedM5PuqJHTp40of-ZDchD7Cc2NTIE2RopgkKifxtRRjQ9wwudz0hxKjVb9E9GCtkaA-MjDdEeVxnSgTu2p8Y9EaPOoZKt-zt0XTjRT8otwx7yOzz1euhDVh1-1zBb7V3Lt-w4BW19draYkGWMzg"


class SearchAndFilterAntibodiesTestCase(TestCase):
    def setUp(self):
        """Set up test user and client"""
        # Create a test user
        self.test_user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        if token:
            set_authentication_token(token)
        
        # Create Django Ninja test client with authenticated user
        self.client = LoggedinTestClient(api, self.test_user)
        self.user_id = "aaaa"  # Use consistent user ID from token
        Member.objects.create(kc_id=self.user_id, user=self.test_user)


    def test_search_and_filter_antibodies(self):
        """Test search and filter via Django Ninja API"""
        # Create antibodies via API
        response = self.client.post("/antibodies", json=example_ab)
        self.assertEqual(response.status_code, 201)
        ab = response.json()
        
        response = self.client.post("/antibodies", json=example_ab2)
        self.assertEqual(response.status_code, 201)
        ab2 = response.json()

        all_antibodies = Antibody.objects.all()
        self.assertEqual(len(all_antibodies), 2)

        # Convert them to curated
        for an in all_antibodies:
            an.status = STATUS.CURATED
            an.save()

        # Create complete filter request
        filter_fts_sort = {
            "search": "N176A",
            "contains": [],
            "equals": [],
            "startsWith": [],
            "endsWith": [],
            "isEmpty": [],
            "isNotEmpty": [],
            "isAnyOf": [],
            "size": 10,
            "page": 1,
            "sortOn": [],
            "operation": "and",
            "isUserScope": False,
        }
        
        # FOR Search alone - catalog number
        response = self.client.post("/search/antibodies", json=filter_fts_sort)
        self.assertEqual(response.status_code, 200)
        result = response.json()
        # Check the count and items
        self.assertEqual(result['totalElements'], 1)
        self.assertEqual(result['items'][0]['catalogNum'], example_ab["catalogNum"])
        self.assertEqual(result['items'][0]['abName'], example_ab["abName"])

        # ONLY SORTING
        filter_fts_sort["search"] = ""
        filter_fts_sort["sortOn"] = [{"key": "catalog_num", "sortorder": "asc"}]
        
        response = self.client.post("/search/antibodies", json=filter_fts_sort)
        self.assertEqual(response.status_code, 200)
        result = response.json()
        self.assertEqual(result['totalElements'], 2)

        # If you check the test data - example_ab.catalogNum is N176A/35
        # and example_ab2.catalogNum is ENCAB558DXQ, hence the order check
        self.assertEqual(result['items'][0]['catalogNum'], example_ab2["catalogNum"])
        self.assertEqual(result['items'][1]['catalogNum'], example_ab["catalogNum"])

        # FILTERING WITH SORTING - No search
        filter_fts_sort["contains"] = [{"key": "catalog_num", "value": "N176A/35"}]
        
        response = self.client.post("/search/antibodies", json=filter_fts_sort)
        self.assertEqual(response.status_code, 200)
        result = response.json()
        self.assertEqual(result['totalElements'], 1)
        self.assertEqual(result['items'][0]['catalogNum'], example_ab["catalogNum"])

        # FILTERING WITH SORTING - search
        filter_fts_sort["search"] = "DXQ"
        
        response = self.client.post("/search/antibodies", json=filter_fts_sort)
        self.assertEqual(response.status_code, 200)
        result = response.json()
        self.assertEqual(result['totalElements'], 0)

        # CHECK ISANY - and foreign key - vendor
        # Should return only one
        filter_fts_sort["sortOn"] = [{"key": "vendor", "sortorder": "asc"}]
        filter_fts_sort["contains"] = []
        filter_fts_sort["isAnyOf"] = [
            {"key": "vendor", "value": ["Andrew Dingwall", "John Doe"]}
        ]
        filter_fts_sort["search"] = ""
        
        response = self.client.post("/search/antibodies", json=filter_fts_sort)
        self.assertEqual(response.status_code, 200)
        result = response.json()
        self.assertEqual(result['totalElements'], 1)
        self.assertEqual(result['items'][0]['catalogNum'], example_ab2["catalogNum"])

        # Should return two
        filter_fts_sort["isAnyOf"] = [
            {"key": "vendor", "value": ["Andrew Dingwall", "My vendorname"]}
        ]
        
        response = self.client.post("/search/antibodies", json=filter_fts_sort)
        self.assertEqual(response.status_code, 200)
        result = response.json()
        self.assertEqual(result['totalElements'], 2)
        # This is first because Andrew Dingwall comes first
        self.assertEqual(result['items'][0]['catalogNum'], example_ab2["catalogNum"])
        self.assertEqual(result['items'][1]['catalogNum'], example_ab["catalogNum"])

        # Test sorting by species
        filter_fts_sort["sortOn"] = [{"key": "species", "sortorder": "desc"}]
        filter_fts_sort["isAnyOf"] = []
        
        response = self.client.post("/search/antibodies", json=filter_fts_sort)
        self.assertEqual(response.status_code, 200)
        result = response.json()
        self.assertEqual(result['totalElements'], 2)
        self.assertEqual(result['items'][0]['catalogNum'], example_ab2["catalogNum"])

        # Check isEmpty and isNotEmpty
        example_ab3 = example_ab.copy()
        example_ab3["catalogNum"] = None
        
        response = self.client.post("/antibodies", json=example_ab3)
        self.assertEqual(response.status_code, 201)
        ab3 = response.json()
        
        # Curate the new antibody
        antibody3 = Antibody.objects.get(ab_id=ab3['abId'])
        antibody3.status = STATUS.CURATED
        antibody3.save()

        filter_fts_sort["isEmpty"] = ["catalog_num"]
        filter_fts_sort["sortOn"] = []
        
        response = self.client.post("/search/antibodies", json=filter_fts_sort)
        self.assertEqual(response.status_code, 200)
        result = response.json()
        self.assertEqual(result['totalElements'], 1)
        self.assertEqual(result['items'][0]['catalogNum'], example_ab3["catalogNum"])

        filter_fts_sort["isEmpty"] = []
        filter_fts_sort["isNotEmpty"] = ["catalog_num"]
        
        response = self.client.post("/search/antibodies", json=filter_fts_sort)
        self.assertEqual(response.status_code, 200)
        result = response.json()
        self.assertEqual(result['totalElements'], 2)

