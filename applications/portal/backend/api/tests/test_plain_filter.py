from django.test import TestCase
from django.contrib.auth.models import User
from .data.test_data import example_ab2, example_ab
from api.api import api
from .utils import LoggedinTestClient
from cloudharness.middleware import set_authentication_token
from cloudharness_django.models import Member


token = "eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICJJUHJQcnZBanBrZ19HQlVUSVN5YVBoaXRMeUtVNDlQUGJRUTlPaWNBWEtzIn0.eyJleHAiOjE3MTAyMzg2MDAsImlhdCI6MTcxMDIyNzgwMCwiYXV0aF90aW1lIjoxNzEwMjI3ODAwLCJqdGkiOiIxZTFkMjRmMy0zMTU3LTRhNzEtOGI4Ny0yNzZhZjBkMGFjMTUiLCJpc3MiOiJodHRwczovL2FjY291bnRzLmFyZWcuZGV2Lm1ldGFjZWxsLnVzL2F1dGgvcmVhbG1zL2FyZWciLCJhdWQiOlsid2ViLWNsaWVudCIsImFjY291bnQiXSwic3ViIjoiNjZhOWRkNTQtMjIxNC00ZWQ3LWI0ZjgtZGFhNWJmM2M5YTc5IiwidHlwIjoiQmVhcmVyIiwiYXpwIjoid2ViLWNsaWVudCIsInNlc3Npb25fc3RhdGUiOiI1MzMyNDQ5MS0zNmY4LTRlODctOGE5YS0yZTIyODc3YmQxMDciLCJhY3IiOiIxIiwiYWxsb3dlZC1vcmlnaW5zIjpbIioiXSwicmVhbG1fYWNjZXNzIjp7InJvbGVzIjpbImFkbWluaXN0cmF0b3IiLCJkZWZhdWx0LXJvbGVzLWFyZWciXX0sInJlc291cmNlX2FjY2VzcyI6eyJhY2NvdW50Ijp7InJvbGVzIjpbIm1hbmFnZS1hY2NvdW50IiwibWFuYWdlLWFjY291bnQtbGlua3MiLCJ2aWV3LXByb2ZpbGUiXX19LCJzY29wZSI6Im9wZW5pZCBwcm9maWxlIGFkbWluaXN0cmF0b3Itc2NvcGUgZW1haWwiLCJzaWQiOiI1MzMyNDQ5MS0zNmY4LTRlODctOGE5YS0yZTIyODc3YmQxMDciLCJlbWFpbF92ZXJpZmllZCI6ZmFsc2UsIm5hbWUiOiJGaWxpcHBvIExlZGRhIiwicHJlZmVycmVkX3VzZXJuYW1lIjoiYSIsImdpdmVuX25hbWUiOiJGaWxpcHBvIiwiZmFtaWx5X25hbWUiOiJMZWRkYSIsImVtYWlsIjoiYUBhYS5pdCJ9.RShiiCZPEwz2IxEQqU2TBB1F6NQIOMfcrVU99eMSlXEahb38VegqUyIqUfoQUrQAHqnyysR67HeBuCq2SNh9ctxpAiEpFq7LAkqpEIQfByvdyDsBArT0jeWd6DuQ91_7PAdSPWqFEr-uFo9476NQZecrIuXCaNC3rrHbPb6GZKwT6gUMu_sCYAawT8jA_V9rpfgedM5PuqJHTp40of-ZDchD7Cc2NTIE2RopgkKifxtRRjQ9wwudz0hxKjVb9E9GCtkaA-MjDdEeVxnSgTu2p8Y9EaPOoZKt-zt0XTjRT8otwx7yOzz1euhDVh1-1zBb7V3Lt-w4BW19draYkGWMzg"


class PlainFilterAntibodiesTestCase(TestCase):
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
        
        self.user_id = "66a9dd54-2214-4ed7-b4f8-daa5bf3c9a79"
        Member.objects.create(kc_id=self.user_id, user=self.test_user)

    def test_plain_filter_antibodies(self):
        """Test plain filter antibodies via Django Ninja API with user scope"""
        # Create antibodies via API
        response = self.client.post("/antibodies", json=example_ab)
        self.assertEqual(response.status_code, 201)
        ab = response.json()
        
        response = self.client.post("/antibodies", json=example_ab2)
        self.assertEqual(response.status_code, 201)
        ab2 = response.json()
        
        example_ab3 = example_ab2.copy()
        example_ab3["catalogNum"] = "FOX176A/35"
        example_ab3["vendorName"] = "FOX"

        response = self.client.post("/antibodies", json=example_ab3)
        self.assertEqual(response.status_code, 201)
        ab3 = response.json()

        # Create filter request with user scope (plain filter)
        filter_sort = {
            "search": "",
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
            "isUserScope": True,
        }
        
        response = self.client.post("/search/antibodies", json=filter_sort)
        if response.status_code != 200:
            print(f"DEBUG: Status code: {response.status_code}")
            print(f"DEBUG: Response content: {response.content}")
            print(f"DEBUG: Response headers: {dict(response.headers)}")
        self.assertEqual(response.status_code, 200)
        result = response.json()
        self.assertEqual(result['totalElements'], 3)
        # Since plain sorting by default "-ix", newest first
        self.assertEqual(result['items'][0]['catalogNum'], example_ab3["catalogNum"])
        self.assertEqual(result['items'][1]['catalogNum'], example_ab2["catalogNum"])
        self.assertEqual(result['items'][0]['vendorName'], example_ab3["vendorName"])

        # FILTERING WITHOUT SORTING
        filter_sort["contains"] = [{"key": "catalog_num", "value": "N176A/35"}]
        
        response = self.client.post("/search/antibodies", json=filter_sort)
        self.assertEqual(response.status_code, 200)
        result = response.json()
        self.assertEqual(result['totalElements'], 1)
        self.assertEqual(result['items'][0]['catalogNum'], example_ab["catalogNum"])

        # FILTERING WITH SORTING
        filter_sort["contains"] = []
        filter_sort["sortOn"] = [{"key": "catalog_num", "sortorder": "asc"}]
        
        response = self.client.post("/search/antibodies", json=filter_sort)
        self.assertEqual(response.status_code, 200)
        result = response.json()
        self.assertEqual(result['totalElements'], 3)

        # ab2 -> ab3 -> ab : ENCAB558DXQ -> FOX176A/35 -> N176A/35
        self.assertEqual(result['items'][0]['vendorName'], example_ab2["vendorName"])
        self.assertEqual(result['items'][1]['catalogNum'], example_ab3["catalogNum"])
        self.assertEqual(result['items'][2]['catalogNum'], example_ab["catalogNum"])

