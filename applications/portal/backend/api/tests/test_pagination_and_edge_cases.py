"""
Tests for pagination, edge cases, and complex filtering scenarios
"""
from django.test import TestCase
from django.contrib.auth.models import User
from unittest.mock import patch

from api.models import Antibody, STATUS, Vendor, Specie, Application
from api.schemas import FilterRequest
from api.routers import antibody, search
from .utils import LoggedinTestClient, AnonymousTestClient
from cloudharness_django.models import Member


class PaginationAndEdgeCasesTestCase(TestCase):
    def setUp(self):
        """Set up test user and client"""
        self.test_user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        # Create combined API for testing
        from ninja import NinjaAPI
        import uuid
        combined_api = NinjaAPI(title="Test API", urls_namespace=f"test_{uuid.uuid4().hex[:8]}")
        antibody.router.api = None
        search.router.api = None
        combined_api.add_router("", antibody.router)
        combined_api.add_router("", search.router)
        from api.helpers.response_helpers import add_exception_handlers
        add_exception_handlers(combined_api)
        
        self.client = LoggedinTestClient(combined_api, self.test_user)
        self.anon_client = AnonymousTestClient(combined_api, User.objects.create_user(username='anon'))
        
        self.user_id = "test-user-id-123"
        Member.objects.create(kc_id=self.user_id, user=self.test_user)
        
        # Mock user ID for serialization
        self.get_user_id_patcher = patch('api.mappers.mapping_utils.get_current_user_id')
        self.mock_get_user_id = self.get_user_id_patcher.start()
        self.mock_get_user_id.return_value = self.user_id

    def tearDown(self):
        """Clean up patches"""
        self.get_user_id_patcher.stop()

    def test_pagination_basic(self):
        """Test basic pagination functionality"""
        # Create 15 curated antibodies
        for i in range(15):
            ab = Antibody.objects.create(
                ab_id=f"{1000 + i}",
                ab_name=f"Antibody {i}",
                catalog_num=f"CAT{i:03d}",
                status=STATUS.CURATED
            )
        
        # Test first page with size 10
        response = self.client.get("/antibodies?page=1&size=10")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        
        self.assertEqual(data['page'], 1)
        self.assertEqual(data['totalElements'], 15)
        self.assertEqual(len(data['items']), 10)
        
        # Test second page
        response = self.client.get("/antibodies?page=2&size=10")
        data = response.json()
        
        self.assertEqual(data['page'], 2)
        self.assertEqual(len(data['items']), 5)

    def test_pagination_edge_cases(self):
        """Test pagination edge cases"""
        # Create 5 curated antibodies
        for i in range(5):
            Antibody.objects.create(
                ab_id=f"{2000 + i}",
                ab_name=f"Edge Antibody {i}",
                status=STATUS.CURATED
            )
        
        # Test page 0 (should return error)
        response = self.client.get("/antibodies?page=0&size=10")
        self.assertEqual(response.status_code, 400)
        
        # Test size 0 (should return error)
        response = self.client.get("/antibodies?page=1&size=0")
        self.assertEqual(response.status_code, 400)
        
        # Test negative page (should return error)
        response = self.client.get("/antibodies?page=-1&size=10")
        self.assertEqual(response.status_code, 400)
        
        # Test page beyond available data
        response = self.client.get("/antibodies?page=100&size=10")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data['items']), 0)

    def test_pagination_default_values(self):
        """Test that default pagination values work correctly"""
        for i in range(3):
            Antibody.objects.create(
                ab_id=f"{3000 + i}",
                ab_name=f"Default Antibody {i}",
                status=STATUS.CURATED
            )
        
        # Test without page and size parameters
        response = self.client.get("/antibodies")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        
        self.assertEqual(data['page'], 1)
        self.assertEqual(len(data['items']), 3)

    def test_pagination_limit_for_anonymous_users(self):
        """Test pagination limits for anonymous users"""
        # Create 600 curated antibodies
        for i in range(100):  # Create fewer for test performance
            Antibody.objects.create(
                ab_id=f"{4000 + i}",
                ab_name=f"Limit Test Antibody {i}",
                status=STATUS.CURATED
            )
        
        # Anonymous user requesting large page * size should fail
        response = self.anon_client.get("/antibodies?page=6&size=100")
        self.assertEqual(response.status_code, 401)
        
        # Authenticated user should be able to access
        response = self.client.get("/antibodies?page=1&size=100")
        self.assertEqual(response.status_code, 200)

    def test_user_antibodies_pagination(self):
        """Test pagination for user-specific antibodies"""
        # Create antibodies for the test user
        for i in range(25):
            Antibody.objects.create(
                ab_id=f"{5000 + i}",
                ab_name=f"User Antibody {i}",
                uid=self.user_id,
                status=STATUS.QUEUE  # User's own antibodies, not curated
            )
        
        # Test first page
        response = self.client.get("/antibodies/user?page=1&size=10")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        
        self.assertEqual(data['page'], 1)
        self.assertEqual(data['totalElements'], 25)
        self.assertEqual(len(data['items']), 10)
        
        # Test page size limit (max 100)
        response = self.client.get("/antibodies/user?page=1&size=150")
        self.assertEqual(response.status_code, 400)

    def test_search_with_pagination(self):
        """Test full-text search with pagination"""
        # Create antibodies with searchable content
        for i in range(20):
            Antibody.objects.create(
                ab_id=f"{6000 + i}",
                ab_name=f"Search Test Antibody {i}",
                catalog_num=f"SEARCH{i:03d}",
                status=STATUS.CURATED
            )
        
        # Refresh search view
        from api.repositories.maintainance import refresh_search_view
        refresh_search_view()
        
        # Search with pagination
        response = self.client.get("/fts-antibodies?q=Search&page=1&size=10")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        
        self.assertEqual(data['page'], 1)
        self.assertEqual(len(data['items']), 10)
        
        # Second page
        response = self.client.get("/fts-antibodies?q=Search&page=2&size=10")
        data = response.json()
        self.assertEqual(len(data['items']), 10)

    def test_filter_with_multiple_conditions(self):
        """Test complex filtering with multiple conditions"""
        # Create vendor and species
        vendor = Vendor.objects.create(vendor="Test Vendor", commercial_type="commercial")
        species1 = Specie.objects.create(name="human")
        species2 = Specie.objects.create(name="mouse")
        
        # Create antibodies with various attributes
        for i in range(10):
            ab = Antibody.objects.create(
                ab_id=f"{7000 + i}",
                ab_name=f"Filter Test {i}",
                catalog_num=f"FT{i:03d}" if i % 2 == 0 else None,
                vendor=vendor,
                status=STATUS.CURATED
            )
            if i < 5:
                ab.species.add(species1)
            else:
                ab.species.add(species2)
        
        # Test contains + isNotEmpty filter
        filter_data = {
            "search": "",
            "contains": [{"key": "ab_name", "value": "Filter"}],
            "equals": [],
            "startsWith": [],
            "endsWith": [],
            "isEmpty": [],
            "isNotEmpty": ["catalog_num"],
            "isAnyOf": [],
            "size": 10,
            "page": 1,
            "sortOn": [],
            "operation": "and",
            "isUserScope": False,
        }
        
        response = self.client.post("/search/antibodies", json=filter_data)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        
        # Should return only antibodies with catalog numbers
        self.assertEqual(data['totalElements'], 5)
        for item in data['items']:
            self.assertIsNotNone(item.get('catalogNum'))

    def test_filter_with_sorting(self):
        """Test filtering combined with sorting"""
        vendor = Vendor.objects.create(vendor="Sort Vendor", commercial_type="commercial")
        
        # Create antibodies with specific catalog numbers for sorting
        catalog_nums = ["ZZZ", "AAA", "MMM", "DDD"]
        for i, cat_num in enumerate(catalog_nums):
            Antibody.objects.create(
                ab_id=f"{8000 + i}",
                ab_name=f"Sort Test {i}",
                catalog_num=cat_num,
                vendor=vendor,
                status=STATUS.CURATED
            )
        
        # Test ascending sort
        filter_data = {
            "search": "",
            "contains": [{"key": "ab_name", "value": "Sort"}],
            "equals": [],
            "startsWith": [],
            "endsWith": [],
            "isEmpty": [],
            "isNotEmpty": [],
            "isAnyOf": [],
            "size": 10,
            "page": 1,
            "sortOn": [{"key": "catalog_num", "sortorder": "asc"}],
            "operation": "and",
            "isUserScope": False,
        }
        
        response = self.client.post("/search/antibodies", json=filter_data)
        data = response.json()
        
        cat_nums_result = [item['catalogNum'] for item in data['items']]
        self.assertEqual(cat_nums_result, ["AAA", "DDD", "MMM", "ZZZ"])
        
        # Test descending sort
        filter_data['sortOn'] = [{"key": "catalog_num", "sortorder": "desc"}]
        response = self.client.post("/search/antibodies", json=filter_data)
        data = response.json()
        
        cat_nums_result = [item['catalogNum'] for item in data['items']]
        self.assertEqual(cat_nums_result, ["ZZZ", "MMM", "DDD", "AAA"])

    def test_empty_search_results(self):
        """Test behavior when search returns no results"""
        # Search for non-existent term
        response = self.client.get("/fts-antibodies?q=NonExistentTerm12345")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        
        self.assertEqual(data['totalElements'], 0)
        self.assertEqual(len(data['items']), 0)

    def test_special_characters_in_search(self):
        """Test search with special characters"""
        ab = Antibody.objects.create(
            ab_id="9001",
            ab_name="Anti-CD45 (Clone: HI30)",
            catalog_num="555482",
            status=STATUS.CURATED
        )
        
        from api.repositories.maintainance import refresh_search_view
        refresh_search_view()
        
        # Search with parentheses
        response = self.client.get("/fts-antibodies?q=HI30")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertGreater(data['totalElements'], 0)
        
        # Search with dash
        response = self.client.get("/fts-antibodies?q=Anti-CD45")
        data = response.json()
        self.assertGreater(data['totalElements'], 0)

    def test_date_filtering(self):
        """Test filtering by date ranges"""
        from datetime import datetime, timedelta
        from django.utils.timezone import make_aware
        
        now = make_aware(datetime.now())
        past = now - timedelta(days=30)
        future = now + timedelta(days=30)
        
        # Create antibodies with different dates
        ab1 = Antibody.objects.create(
            ab_id="10001",
            ab_name="Old Antibody",
            status=STATUS.CURATED
        )
        ab1.lastedit_time = past
        ab1.save()
        
        ab2 = Antibody.objects.create(
            ab_id="10002",
            ab_name="Recent Antibody",
            status=STATUS.CURATED
        )
        ab2.lastedit_time = now
        ab2.save()
        
        # Test filtering by updated_from
        response = self.client.get(f"/antibodies?updatedFrom={past.isoformat()}")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['totalElements'], 2)
        
        # Test filtering by updated_to
        response = self.client.get(f"/antibodies?updatedTo={past.isoformat()}")
        data = response.json()
        self.assertEqual(data['totalElements'], 1)

    def test_accession_number_lookup(self):
        """Test looking up antibodies by accession number"""
        ab = Antibody.objects.create(
            ab_id="11001",
            accession="11001",
            ab_name="Accession Test",
            status=STATUS.CURATED
        )
        
        # Test successful lookup
        response = self.client.get(f"/antibodies/user/{ab.accession}")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['abId'], str(ab.ab_id))
        self.assertEqual(data['accession'], str(ab.accession))
        
        # Test lookup of non-existent accession
        response = self.client.get("/antibodies/user/99999999")
        self.assertEqual(response.status_code, 404)

    def test_ab_id_search(self):
        """Test searching by AB_ prefix"""
        ab = Antibody.objects.create(
            ab_id="12001",
            accession="12001",
            ab_name="AB ID Test",
            status=STATUS.CURATED
        )
        
        # Search using AB_ prefix
        response = self.client.get("/fts-antibodies?q=AB_12001")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        
        self.assertGreater(data['totalElements'], 0)
        found = any(item['abId'] == '12001' for item in data['items'])
        self.assertTrue(found)
