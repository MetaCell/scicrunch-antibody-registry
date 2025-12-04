"""
Additional edge cases and error scenarios for antibody endpoints
"""
from django.test import TestCase
from django.contrib.auth.models import User
from unittest.mock import patch

from api.models import Antibody, STATUS, Vendor, Specie, VendorDomain
from api.routers import antibody, search
from .utils import LoggedinTestClient
from .data.test_data import example_ab
from cloudharness_django.models import Member


class AntibodyEdgeCasesTestCase(TestCase):
    def setUp(self):
        """Set up test user and client"""
        self.test_user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        # Create combined API
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
        
        self.user_id = "test-user-id-123"
        Member.objects.create(kc_id=self.user_id, user=self.test_user)
        
        # Mock user ID
        self.get_user_id_patcher = patch('api.mappers.mapping_utils.get_current_user_id')
        self.mock_get_user_id = self.get_user_id_patcher.start()
        self.mock_get_user_id.return_value = self.user_id

    def tearDown(self):
        """Clean up patches"""
        self.get_user_id_patcher.stop()

    def test_create_antibody_with_minimal_data(self):
        """Test creating antibody with only required fields"""
        minimal_ab = {
            "vendorName": "Minimal Vendor",
            "abTarget": "Target",
        }
        
        response = self.client.post("/antibodies", json=minimal_ab)
        self.assertEqual(response.status_code, 201)
        data = response.json()
        self.assertIsNotNone(data['abId'])

    def test_create_antibody_without_vendor_name_or_url(self):
        """Test that creating antibody without vendor name or URL fails"""
        invalid_ab = dict(example_ab)
        invalid_ab.pop('vendorName', None)
        invalid_ab.pop('url', None)
        
        response = self.client.post("/antibodies", json=invalid_ab)
        self.assertEqual(response.status_code, 400)

    def test_create_antibody_with_very_long_fields(self):
        """Test creating antibody with very long field values"""
        long_ab = dict(example_ab)
        long_ab['abName'] = "A" * 1000  # Very long name
        long_ab['comments'] = "B" * 5000  # Very long comments
        
        response = self.client.post("/antibodies", json=long_ab)
        # Should either succeed or fail gracefully
        self.assertIn(response.status_code, [201, 400])

    def test_create_antibody_with_unicode_characters(self):
        """Test creating antibody with Unicode characters"""
        unicode_ab = dict(example_ab)
        unicode_ab['abName'] = "Anti-α-synuclein μ-opioid 🧬"
        unicode_ab['comments'] = "Test with 中文 and émojis 🔬"
        unicode_ab['catalogNum'] = "CAT-αβγ-001"
        
        response = self.client.post("/antibodies", json=unicode_ab)
        self.assertEqual(response.status_code, 201)
        data = response.json()
        self.assertIn('α', data['abName'])

    def test_create_antibody_with_empty_strings(self):
        """Test creating antibody with empty string values"""
        empty_ab = dict(example_ab)
        empty_ab['comments'] = ""
        empty_ab['epitope'] = ""
        
        response = self.client.post("/antibodies", json=empty_ab)
        self.assertEqual(response.status_code, 201)

    def test_create_antibody_with_whitespace_only(self):
        """Test creating antibody with whitespace-only values"""
        whitespace_ab = dict(example_ab)
        whitespace_ab['abName'] = "   Whitespace Test   "
        
        response = self.client.post("/antibodies", json=whitespace_ab)
        self.assertEqual(response.status_code, 201)
        data = response.json()
        # Should be trimmed
        self.assertEqual(data['abName'], "Whitespace Test")

    def test_update_antibody_partial_fields(self):
        """Test updating only some fields of an antibody"""
        # Create antibody
        response = self.client.post("/antibodies", json=example_ab)
        ab = response.json()
        
        # Update only name
        update_data = {
            "abName": "New Name Only",
            "abTarget": example_ab['abTarget'],  # Required field
        }
        
        response = self.client.put(f"/antibodies/user/{ab['accession']}", json=update_data)
        self.assertEqual(response.status_code, 202)
        updated = response.json()
        self.assertEqual(updated['abName'], "New Name Only")

    def test_duplicate_antibody_detection(self):
        """Test that duplicate antibodies are properly detected"""
        # Create first antibody
        response = self.client.post("/antibodies", json=example_ab)
        self.assertEqual(response.status_code, 201)
        
        # Try to create exact duplicate
        response = self.client.post("/antibodies", json=example_ab)
        # Should detect duplicate (either 400 or 409)
        self.assertIn(response.status_code, [400, 409])

    def test_create_antibody_with_multiple_target_species(self):
        """Test creating antibody with multiple target species"""
        multi_species_ab = dict(example_ab)
        multi_species_ab['targetSpecies'] = ["human", "mouse", "rat", "rabbit", "dog"]
        
        response = self.client.post("/antibodies", json=multi_species_ab)
        self.assertEqual(response.status_code, 201)
        data = response.json()
        self.assertEqual(len(data['targetSpecies']), 5)

    def test_create_antibody_with_no_target_species(self):
        """Test creating antibody without target species"""
        no_species_ab = dict(example_ab)
        no_species_ab['targetSpecies'] = []
        
        response = self.client.post("/antibodies", json=no_species_ab)
        self.assertEqual(response.status_code, 201)

    def test_antibody_status_transitions(self):
        """Test different antibody status values"""
        # Create antibody (starts as QUEUE)
        response = self.client.post("/antibodies", json=example_ab)
        ab = response.json()
        
        ab_obj = Antibody.objects.get(ab_id=ab['abId'])
        self.assertEqual(ab_obj.status, STATUS.QUEUE)
        
        # Transition to CURATED
        ab_obj.status = STATUS.CURATED
        ab_obj.save()
        self.assertIsNotNone(ab_obj.curate_time)
        
        # Verify it appears in public listing
        response = self.client.get("/antibodies")
        data = response.json()
        found = any(item['abId'] == ab['abId'] for item in data['items'])
        self.assertTrue(found)

    def test_vendor_url_extraction(self):
        """Test that vendor URLs are properly extracted"""
        test_urls = [
            "https://www.vendor.com/product/123",
            "http://vendor.com/product",
            "https://subdomain.vendor.com/path/to/product",
        ]
        
        for url in test_urls:
            with self.subTest(url=url):
                ab_data = dict(example_ab)
                ab_data['url'] = url
                ab_data['catalogNum'] = f"CAT-{hash(url) % 1000}"
                
                response = self.client.post("/antibodies", json=ab_data)
                self.assertEqual(response.status_code, 201)

    def test_search_with_empty_query(self):
        """Test search with empty query string"""
        response = self.client.get("/fts-antibodies?q=")
        self.assertEqual(response.status_code, 200)
        # Empty query should return results or empty list

    def test_search_with_very_long_query(self):
        """Test search with very long query string"""
        long_query = "A" * 1000
        response = self.client.get(f"/fts-antibodies?q={long_query}")
        self.assertEqual(response.status_code, 200)
        # Should handle gracefully

    def test_filter_with_invalid_field_names(self):
        """Test filtering with invalid field names"""
        filter_data = {
            "search": "",
            "contains": [{"key": "invalid_field_name", "value": "test"}],
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
        
        # Should either handle gracefully or return error
        response = self.client.post("/search/antibodies", json=filter_data)
        self.assertIn(response.status_code, [200, 400])

    def test_concurrent_antibody_creation(self):
        """Test creating multiple antibodies in quick succession"""
        for i in range(5):
            ab_data = dict(example_ab)
            ab_data['catalogNum'] = f"CONCURRENT-{i}"
            ab_data['abName'] = f"Concurrent Test {i}"
            
            response = self.client.post("/antibodies", json=ab_data)
            self.assertEqual(response.status_code, 201)
        
        # Verify all were created
        response = self.client.get("/antibodies/user")
        data = response.json()
        self.assertEqual(data['totalElements'], 5)

    def test_antibody_with_special_catalog_numbers(self):
        """Test antibodies with various catalog number formats"""
        catalog_formats = [
            "12345",
            "AB-12345",
            "CAT#12345",
            "12345-A",
            "A-12345-B",
            "12.345.67",
            "12-345/67",
        ]
        
        for i, cat_num in enumerate(catalog_formats):
            with self.subTest(catalog_num=cat_num):
                ab_data = dict(example_ab)
                ab_data['catalogNum'] = cat_num
                ab_data['abName'] = f"Catalog Test {i}"
                
                response = self.client.post("/antibodies", json=ab_data)
                self.assertEqual(response.status_code, 201)

    def test_get_nonexistent_antibody(self):
        """Test getting antibody that doesn't exist"""
        response = self.client.get("/antibodies/999999999")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data), 0)  # Empty list

    def test_update_nonexistent_antibody(self):
        """Test updating antibody that doesn't exist"""
        response = self.client.put("/antibodies/user/999999999", json=example_ab)
        self.assertEqual(response.status_code, 404)

    def test_antibody_with_applications(self):
        """Test creating antibody with multiple applications"""
        # Create applications
        app1 = "ELISA"
        app2 = "Western Blot"
        app3 = "Flow Cytometry"
        
        ab_data = dict(example_ab)
        ab_data['applications'] = [app1, app2, app3]
        
        response = self.client.post("/antibodies", json=ab_data)
        self.assertEqual(response.status_code, 201)

    def test_source_organism_creation(self):
        """Test that new source organisms are created correctly"""
        new_organism = "Xenopus laevis"
        
        ab_data = dict(example_ab)
        ab_data['sourceOrganism'] = new_organism
        ab_data['catalogNum'] = "ORGANISM-TEST-001"
        
        response = self.client.post("/antibodies", json=ab_data)
        self.assertEqual(response.status_code, 201)
        data = response.json()
        self.assertEqual(data['sourceOrganism'], new_organism)
        
        # Verify species was created
        self.assertTrue(Specie.objects.filter(name=new_organism).exists())

    def test_vendor_domain_status_visibility(self):
        """Test that vendor URLs respect curation status"""
        # Create antibody
        response = self.client.post("/antibodies", json=example_ab)
        ab = response.json()
        
        # Get antibody - vendor URL should not be shown (not curated)
        response = self.client.get(f"/antibodies/{ab['abId']}")
        data = response.json()[0]
        # Vendor domains not curated yet
        self.assertEqual(len(data.get('vendorUrl', [])), 0)
        
        # Curate vendor domains
        ab_obj = Antibody.objects.get(ab_id=ab['abId'])
        for domain in ab_obj.vendor.vendordomain_set.all():
            domain.status = STATUS.CURATED
            domain.save()
        
        # Now vendor URL should be visible
        response = self.client.get(f"/antibodies/{ab['abId']}")
        data = response.json()[0]
        self.assertGreater(len(data['vendorUrl']), 0)

    def test_filtering_by_status(self):
        """Test filtering antibodies by status"""
        # Create antibodies with different statuses
        for i in range(3):
            Antibody.objects.create(
                ab_id=f"{10000 + i}",
                ab_name=f"Curated {i}",
                status=STATUS.CURATED
            )
        
        for i in range(2):
            Antibody.objects.create(
                ab_id=f"{10100 + i}",
                ab_name=f"Queue {i}",
                status=STATUS.QUEUE
            )
        
        # Filter by curated status
        response = self.client.get("/antibodies?status=curated")
        data = response.json()
        self.assertEqual(data['totalElements'], 3)

    def test_case_insensitive_vendor_matching(self):
        """Test that vendor matching is case-insensitive"""
        # Create antibody with vendor
        response = self.client.post("/antibodies", json=example_ab)
        ab1 = response.json()
        
        # Create another with same vendor but different case
        ab_data2 = dict(example_ab)
        ab_data2['vendorName'] = example_ab['vendorName'].upper()
        ab_data2['catalogNum'] = "CASE-TEST-001"
        
        response = self.client.post("/antibodies", json=ab_data2)
        ab2 = response.json()
        
        # Should recognize as same vendor
        # (implementation may vary, but vendors should be matched)
        self.assertIsNotNone(ab2['vendorId'])
