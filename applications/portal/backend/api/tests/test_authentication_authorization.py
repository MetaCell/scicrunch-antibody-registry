"""
Tests for authentication and authorization scenarios
"""
from django.test import TestCase
from django.contrib.auth.models import User
from unittest.mock import patch

from api.models import Antibody, STATUS, Vendor
from api.routers import antibody, search
from .utils import LoggedinTestClient, AnonymousTestClient
from .data.test_data import example_ab
from cloudharness_django.models import Member


class AuthenticationAuthorizationTestCase(TestCase):
    def setUp(self):
        """Set up test users and clients"""
        # Regular user
        self.test_user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        # Admin user
        self.admin_user = User.objects.create_user(
            username='admin',
            email='admin@example.com',
            password='admin123',
            is_staff=True,
            is_superuser=True
        )
        
        # Another regular user
        self.other_user = User.objects.create_user(
            username='otheruser',
            email='other@example.com',
            password='other123'
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
        
        # Create clients
        self.client = LoggedinTestClient(combined_api, self.test_user)
        self.admin_client = LoggedinTestClient(combined_api, self.admin_user)
        self.other_client = LoggedinTestClient(combined_api, self.other_user)
        self.anon_client = AnonymousTestClient(combined_api, User.objects.create_user(username='anon'))
        
        # Create members
        self.user_id = "test-user-id-123"
        self.admin_id = "admin-user-id-456"
        self.other_user_id = "other-user-id-789"
        Member.objects.create(kc_id=self.user_id, user=self.test_user)
        Member.objects.create(kc_id=self.admin_id, user=self.admin_user)
        Member.objects.create(kc_id=self.other_user_id, user=self.other_user)
        
        # Mock user ID
        self.get_user_id_patcher = patch('api.mappers.mapping_utils.get_current_user_id')
        self.mock_get_user_id = self.get_user_id_patcher.start()
        self.mock_get_user_id.return_value = self.user_id

    def tearDown(self):
        """Clean up patches"""
        self.get_user_id_patcher.stop()

    def test_anonymous_can_view_curated_antibodies(self):
        """Test that anonymous users can view curated antibodies"""
        # Create curated antibody
        ab = Antibody.objects.create(
            ab_id="1001",
            ab_name="Public Antibody",
            status=STATUS.CURATED
        )
        
        response = self.anon_client.get("/antibodies")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['totalElements'], 1)

    def test_anonymous_cannot_view_queue_antibodies(self):
        """Test that anonymous users cannot see queue antibodies in public list"""
        # Create queue antibody
        ab = Antibody.objects.create(
            ab_id="1002",
            ab_name="Queue Antibody",
            uid=self.user_id,
            status=STATUS.QUEUE
        )
        
        response = self.anon_client.get("/antibodies")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['totalElements'], 0)  # Queue antibodies not shown

    def test_anonymous_cannot_create_antibody(self):
        """Test that anonymous users cannot create antibodies"""
        response = self.anon_client.post("/antibodies", json=example_ab)
        self.assertEqual(response.status_code, 401)

    def test_authenticated_user_can_create_antibody(self):
        """Test that authenticated users can create antibodies"""
        response = self.client.post("/antibodies", json=example_ab)
        self.assertEqual(response.status_code, 201)

    def test_user_can_view_own_queue_antibodies(self):
        """Test that users can view their own queue antibodies"""
        # Create antibody for test user
        ab = Antibody.objects.create(
            ab_id="2001",
            ab_name="My Queue Antibody",
            uid=self.user_id,
            status=STATUS.QUEUE
        )
        
        # User should see it via /antibodies/{ab_id}
        response = self.client.get(f"/antibodies/{ab.ab_id}")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertGreater(len(data), 0)

    def test_user_cannot_view_others_queue_antibodies(self):
        """Test that users cannot view other users' queue antibodies"""
        # Create antibody for other user
        ab = Antibody.objects.create(
            ab_id="2002",
            ab_name="Other User Queue Antibody",
            uid=self.other_user_id,
            status=STATUS.QUEUE
        )
        
        # Test user should not see it
        response = self.client.get(f"/antibodies/{ab.ab_id}")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data), 0)  # Empty list

    def test_user_antibodies_endpoint_requires_auth(self):
        """Test that /antibodies/user endpoint requires authentication"""
        response = self.anon_client.get("/antibodies/user")
        self.assertEqual(response.status_code, 401)

    def test_user_can_only_see_own_antibodies(self):
        """Test that /antibodies/user only returns user's own antibodies"""
        # Create antibodies for different users
        ab1 = Antibody.objects.create(
            ab_id="3001",
            ab_name="My Antibody",
            uid=self.user_id,
            status=STATUS.QUEUE
        )
        
        ab2 = Antibody.objects.create(
            ab_id="3002",
            ab_name="Other User Antibody",
            uid=self.other_user_id,
            status=STATUS.QUEUE
        )
        
        response = self.client.get("/antibodies/user")
        data = response.json()
        
        self.assertEqual(data['totalElements'], 1)
        self.assertEqual(data['items'][0]['abId'], str(ab1.ab_id))

    def test_user_can_only_update_own_antibodies(self):
        """Test that users can only update their own antibodies"""
        # Create antibody for other user
        ab = Antibody.objects.create(
            ab_id="4001",
            ab_name="Other User Antibody",
            accession="4001",
            uid=self.other_user_id,
            status=STATUS.QUEUE
        )
        
        # Try to update with test user
        update_data = dict(example_ab)
        update_data["abName"] = "Hacked Name"
        
        response = self.client.put(f"/antibodies/user/{ab.accession}", json=update_data)
        self.assertEqual(response.status_code, 404)  # Not found for this user

    def test_user_can_update_own_antibodies(self):
        """Test that users can update their own antibodies"""
        # Create antibody for test user
        ab = Antibody.objects.create(
            ab_id="4002",
            ab_name="My Antibody",
            accession="4002",
            uid=self.user_id,
            status=STATUS.QUEUE
        )
        
        # Update with test user
        update_data = dict(example_ab)
        update_data["abName"] = "Updated Name"
        
        response = self.client.put(f"/antibodies/user/{ab.accession}", json=update_data)
        self.assertEqual(response.status_code, 202)
        data = response.json()
        self.assertEqual(data['abName'], "Updated Name")

    def test_anonymous_search_pagination_limit(self):
        """Test that anonymous users have pagination limits"""
        # Create many antibodies
        for i in range(100):
            Antibody.objects.create(
                ab_id=f"{5000 + i}",
                ab_name=f"Antibody {i}",
                status=STATUS.CURATED
            )
        
        # Anonymous user with large page * size should fail
        response = self.anon_client.get("/antibodies?page=6&size=100")
        self.assertEqual(response.status_code, 401)
        
        # Authenticated user should succeed
        response = self.client.get("/antibodies?page=6&size=100")
        self.assertEqual(response.status_code, 200)

    @patch('api.services.user_service.check_if_user_is_admin')
    def test_admin_export_requires_admin_role(self, mock_check_admin):
        """Test that admin export requires admin role"""
        # Regular user should be denied
        mock_check_admin.return_value = False
        response = self.client.get("/antibodies/export/admin")
        self.assertEqual(response.status_code, 401)
        
        # Admin user should be allowed
        mock_check_admin.return_value = True
        with patch('api.services.filesystem_service.check_if_file_does_not_exist_and_recent'):
            with patch('api.services.export_service.generate_antibodies_fields_by_status_to_csv'):
                response = self.admin_client.get("/antibodies/export/admin")
                self.assertEqual(response.status_code, 302)

    def test_search_accessible_to_all(self):
        """Test that search endpoints are accessible to all users"""
        # Create test data
        ab = Antibody.objects.create(
            ab_id="6001",
            ab_name="Search Test",
            catalog_num="SEARCH001",
            status=STATUS.CURATED
        )
        
        from api.repositories.maintainance import refresh_search_view
        refresh_search_view()
        
        # Anonymous user
        response = self.anon_client.get("/fts-antibodies?q=Search")
        self.assertEqual(response.status_code, 200)
        
        # Authenticated user
        response = self.client.get("/fts-antibodies?q=Search")
        self.assertEqual(response.status_code, 200)

    def test_filter_search_accessible_to_all(self):
        """Test that filter search is accessible to all users"""
        ab = Antibody.objects.create(
            ab_id="7001",
            ab_name="Filter Test",
            status=STATUS.CURATED
        )
        
        filter_data = {
            "search": "",
            "contains": [{"key": "ab_name", "value": "Filter"}],
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
        
        # Anonymous user
        response = self.anon_client.post("/search/antibodies", json=filter_data)
        self.assertEqual(response.status_code, 200)
        
        # Authenticated user
        response = self.client.post("/search/antibodies", json=filter_data)
        self.assertEqual(response.status_code, 200)

    def test_user_scope_filter_respects_authentication(self):
        """Test that user scope filtering works correctly"""
        # Create antibodies for different users
        ab1 = Antibody.objects.create(
            ab_id="8001",
            ab_name="User 1 Antibody",
            uid=self.user_id,
            status=STATUS.QUEUE
        )
        
        ab2 = Antibody.objects.create(
            ab_id="8002",
            ab_name="User 2 Antibody",
            uid=self.other_user_id,
            status=STATUS.QUEUE
        )
        
        # Filter with user scope
        filter_data = {
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
            "isUserScope": True,  # User scope enabled
        }
        
        response = self.client.post("/search/antibodies", json=filter_data)
        data = response.json()
        
        # Should only return test user's antibodies
        self.assertEqual(data['totalElements'], 1)
        self.assertEqual(data['items'][0]['abId'], str(ab1.ab_id))

    def test_get_by_accession_requires_ownership(self):
        """Test that accession lookup requires ownership for non-curated antibodies"""
        # Create non-curated antibody for other user
        ab = Antibody.objects.create(
            ab_id="9001",
            ab_name="Other User Antibody",
            accession="9001",
            uid=self.other_user_id,
            status=STATUS.QUEUE
        )
        
        # Test user should not be able to access it
        response = self.client.get(f"/antibodies/user/{ab.accession}")
        self.assertEqual(response.status_code, 404)
        
        # Other user should be able to access it
        self.mock_get_user_id.return_value = self.other_user_id
        response = self.other_client.get(f"/antibodies/user/{ab.accession}")
        self.assertEqual(response.status_code, 200)

    def test_curated_antibodies_accessible_to_all_via_accession(self):
        """Test that curated antibodies are accessible to all via accession lookup"""
        ab = Antibody.objects.create(
            ab_id="10001",
            ab_name="Curated Antibody",
            accession="10001",
            uid=self.other_user_id,
            status=STATUS.CURATED
        )
        
        # Any authenticated user can access curated antibodies
        response = self.client.get(f"/antibodies/user/{ab.accession}")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['abId'], str(ab.ab_id))
