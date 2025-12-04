"""
Tests for search endpoints (species, applications, vendors)
"""
from django.test import TestCase
from django.contrib.auth.models import User

from api.models import Specie, Application, Vendor
from api.routers import search
from .utils import LoggedinTestClient, AnonymousTestClient
from cloudharness_django.models import Member


class SearchEndpointsTestCase(TestCase):
    def setUp(self):
        """Set up test user and client"""
        self.test_user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        # Create test clients
        self.client = LoggedinTestClient(search.router, self.test_user)
        self.anon_client = AnonymousTestClient(search.router, User.objects.create_user(username='anon'))
        
        self.user_id = "test-user-id-123"
        Member.objects.create(kc_id=self.user_id, user=self.test_user)

    def test_get_species(self):
        """Test GET /species endpoint"""
        # Create test species
        species_names = ["human", "mouse", "rat", "rabbit", "Drosophila melanogaster"]
        for name in species_names:
            Specie.objects.create(name=name)
        
        # Test with authenticated user
        response = self.client.get("/species")
        self.assertEqual(response.status_code, 200)
        species = response.json()
        
        self.assertEqual(len(species), 5)
        # Should be ordered by name
        self.assertEqual(species[0], "Drosophila melanogaster")
        self.assertIn("human", species)
        self.assertIn("mouse", species)
        
        # Test with anonymous user
        response = self.anon_client.get("/species")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 5)

    def test_get_species_empty(self):
        """Test GET /species with no species in database"""
        response = self.client.get("/species")
        self.assertEqual(response.status_code, 200)
        species = response.json()
        self.assertEqual(len(species), 0)

    def test_get_species_ordering(self):
        """Test that species are returned in alphabetical order"""
        # Create species in random order
        species_names = ["zebra", "aardvark", "mouse", "Human", "Ant"]
        for name in species_names:
            Specie.objects.create(name=name)
        
        response = self.client.get("/species")
        species = response.json()
        
        # Check ordering (case-insensitive alphabetical)
        for i in range(len(species) - 1):
            self.assertLessEqual(species[i].lower(), species[i + 1].lower())

    def test_get_applications(self):
        """Test GET /applications endpoint"""
        # Create test applications
        app_names = ["ELISA", "IHC", "WB", "Flow Cytometry", "ICC"]
        for name in app_names:
            Application.objects.create(name=name)
        
        # Test with authenticated user
        response = self.client.get("/applications")
        self.assertEqual(response.status_code, 200)
        applications = response.json()
        
        self.assertEqual(len(applications), 5)
        self.assertIn("ELISA", applications)
        self.assertIn("Flow Cytometry", applications)
        
        # Test with anonymous user
        response = self.anon_client.get("/applications")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 5)

    def test_get_applications_empty(self):
        """Test GET /applications with no applications in database"""
        response = self.client.get("/applications")
        self.assertEqual(response.status_code, 200)
        applications = response.json()
        self.assertEqual(len(applications), 0)

    def test_get_applications_ordering(self):
        """Test that applications are returned in alphabetical order"""
        # Create applications in random order
        app_names = ["Western Blot", "ELISA", "IHC", "ChIP", "Immunofluorescence"]
        for name in app_names:
            Application.objects.create(name=name)
        
        response = self.client.get("/applications")
        applications = response.json()
        
        # Check ordering
        for i in range(len(applications) - 1):
            self.assertLessEqual(applications[i].lower(), applications[i + 1].lower())

    def test_get_vendors(self):
        """Test GET /vendors endpoint"""
        # Create test vendors
        vendor1 = Vendor.objects.create(
            vendor="Abcam",
            commercial_type="commercial"
        )
        vendor2 = Vendor.objects.create(
            vendor="Cell Signaling Technology",
            commercial_type="commercial"
        )
        vendor3 = Vendor.objects.create(
            vendor="Santa Cruz Biotechnology",
            commercial_type="commercial"
        )
        
        # Test with authenticated user
        response = self.client.get("/vendors")
        self.assertEqual(response.status_code, 200)
        vendors = response.json()
        
        self.assertEqual(len(vendors), 3)
        
        # Check vendor structure
        vendor_names = [v['vendor'] for v in vendors]
        self.assertIn("Abcam", vendor_names)
        self.assertIn("Cell Signaling Technology", vendor_names)
        
        # Verify all vendors have required fields
        for vendor in vendors:
            self.assertIn('id', vendor)
            self.assertIn('vendor', vendor)
            self.assertIn('commercialType', vendor)
        
        # Test with anonymous user
        response = self.anon_client.get("/vendors")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 3)

    def test_get_vendors_empty(self):
        """Test GET /vendors with no vendors in database"""
        response = self.client.get("/vendors")
        self.assertEqual(response.status_code, 200)
        vendors = response.json()
        self.assertEqual(len(vendors), 0)

    def test_get_vendors_ordering(self):
        """Test that vendors are returned in alphabetical order"""
        # Create vendors in random order
        vendor_names = ["Zymed", "Abcam", "Millipore", "BD Biosciences"]
        for name in vendor_names:
            Vendor.objects.create(vendor=name, commercial_type="commercial")
        
        response = self.client.get("/vendors")
        vendors = response.json()
        
        # Check ordering
        vendor_names_result = [v['vendor'] for v in vendors]
        for i in range(len(vendor_names_result) - 1):
            self.assertLessEqual(vendor_names_result[i].lower(), vendor_names_result[i + 1].lower())

    def test_get_vendors_different_commercial_types(self):
        """Test GET /vendors with different commercial types"""
        Vendor.objects.create(vendor="Commercial Vendor", commercial_type="commercial")
        Vendor.objects.create(vendor="Non-Commercial Vendor", commercial_type="noncommercial")
        Vendor.objects.create(vendor="Addgene", commercial_type="commercial")
        
        response = self.client.get("/vendors")
        vendors = response.json()
        
        self.assertEqual(len(vendors), 3)
        
        # Check that commercial types are properly set
        commercial_vendor = next(v for v in vendors if v['vendor'] == 'Commercial Vendor')
        self.assertEqual(commercial_vendor['commercialType'], 'commercial')
        
        noncommercial_vendor = next(v for v in vendors if v['vendor'] == 'Non-Commercial Vendor')
        self.assertEqual(noncommercial_vendor['commercialType'], 'noncommercial')

    def test_all_search_endpoints_accessible_without_auth(self):
        """Verify all search endpoints are accessible without authentication"""
        # Populate some test data
        Specie.objects.create(name="test_species")
        Application.objects.create(name="test_application")
        Vendor.objects.create(vendor="test_vendor", commercial_type="commercial")
        
        endpoints = ["/species", "/applications", "/vendors"]
        
        for endpoint in endpoints:
            with self.subTest(endpoint=endpoint):
                response = self.anon_client.get(endpoint)
                self.assertEqual(response.status_code, 200)
                data = response.json()
                self.assertIsInstance(data, list)
                self.assertGreater(len(data), 0)
