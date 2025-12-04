"""
Tests for export endpoints and CSV generation
"""
import os
import tempfile
from django.test import TestCase
from django.contrib.auth.models import User
from unittest.mock import patch, MagicMock

from api.models import Antibody, STATUS, Vendor
from api.routers import antibody
from .utils import LoggedinTestClient
from cloudharness_django.models import Member


class ExportEndpointsTestCase(TestCase):
    def setUp(self):
        """Set up test user and client"""
        self.test_user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        # Create admin user
        self.admin_user = User.objects.create_user(
            username='admin',
            email='admin@example.com',
            password='admin123',
            is_staff=True,
            is_superuser=True
        )
        
        self.client = LoggedinTestClient(antibody.router, self.test_user)
        self.admin_client = LoggedinTestClient(antibody.router, self.admin_user)
        
        self.user_id = "test-user-id-123"
        self.admin_id = "admin-user-id-456"
        Member.objects.create(kc_id=self.user_id, user=self.test_user)
        Member.objects.create(kc_id=self.admin_id, user=self.admin_user)
        
        # Mock user ID for serialization
        self.get_user_id_patcher = patch('api.mappers.mapping_utils.get_current_user_id')
        self.mock_get_user_id = self.get_user_id_patcher.start()
        self.mock_get_user_id.return_value = self.user_id

    def tearDown(self):
        """Clean up patches"""
        self.get_user_id_patcher.stop()

    def test_export_antibodies_post(self):
        """Test POST /antibodies/export endpoint"""
        # Create some curated antibodies
        vendor = Vendor.objects.create(vendor="Export Vendor", commercial_type="commercial")
        for i in range(5):
            Antibody.objects.create(
                ab_id=f"{1000 + i}",
                ab_name=f"Export Antibody {i}",
                catalog_num=f"EXP{i:03d}",
                vendor=vendor,
                status=STATUS.CURATED
            )
        
        # Test export
        response = self.client.post("/antibodies/export")
        self.assertEqual(response.status_code, 200)
        
        # Response should be CSV content
        csv_content = response.json()
        self.assertIsInstance(csv_content, str)
        
        # Check CSV contains expected headers and data
        lines = csv_content.split('\n')
        self.assertGreater(len(lines), 1)  # At least header + data
        
        # Header should contain expected columns
        header = lines[0]
        self.assertIn('rrid', header.lower())

    @patch('api.services.user_service.check_if_user_is_admin')
    def test_export_admin_unauthorized(self, mock_check_admin):
        """Test that non-admin users cannot access admin export"""
        mock_check_admin.return_value = False
        
        response = self.client.get("/antibodies/export/admin")
        self.assertEqual(response.status_code, 401)

    @patch('api.services.user_service.check_if_user_is_admin')
    def test_export_admin_authorized(self, mock_check_admin):
        """Test that admin users can access admin export"""
        mock_check_admin.return_value = True
        
        # Create test antibodies
        vendor = Vendor.objects.create(vendor="Admin Export Vendor", commercial_type="commercial")
        for i in range(3):
            Antibody.objects.create(
                ab_id=f"{2000 + i}",
                ab_name=f"Admin Export Antibody {i}",
                catalog_num=f"ADMIN{i:03d}",
                vendor=vendor,
                status=STATUS.CURATED
            )
        
        with patch('api.services.filesystem_service.check_if_file_does_not_exist_and_recent') as mock_file_check:
            mock_file_check.return_value = True
            with patch('api.services.export_service.generate_antibodies_fields_by_status_to_csv'):
                response = self.admin_client.get("/antibodies/export/admin")
                # Should redirect to the CSV file
                self.assertEqual(response.status_code, 302)

    @patch('api.services.user_service.check_if_user_is_admin')
    def test_export_admin_with_status_filter(self, mock_check_admin):
        """Test admin export with status filtering"""
        mock_check_admin.return_value = True
        
        # Create antibodies with different statuses
        vendor = Vendor.objects.create(vendor="Status Export Vendor", commercial_type="commercial")
        
        for i in range(3):
            Antibody.objects.create(
                ab_id=f"{3000 + i}",
                ab_name=f"Curated {i}",
                vendor=vendor,
                status=STATUS.CURATED
            )
        
        for i in range(2):
            Antibody.objects.create(
                ab_id=f"{3100 + i}",
                ab_name=f"Queue {i}",
                vendor=vendor,
                status=STATUS.QUEUE
            )
        
        with patch('api.services.filesystem_service.check_if_file_does_not_exist_and_recent') as mock_file_check:
            mock_file_check.return_value = True
            with patch('api.services.export_service.generate_antibodies_fields_by_status_to_csv') as mock_export:
                response = self.admin_client.get("/antibodies/export/admin?status=curated")
                self.assertEqual(response.status_code, 302)
                # Verify the export function was called with correct status
                mock_export.assert_called_once()

    def test_export_regular_endpoint(self):
        """Test GET /antibodies/export endpoint"""
        # Create test antibodies
        vendor = Vendor.objects.create(vendor="Regular Export Vendor", commercial_type="commercial")
        for i in range(3):
            Antibody.objects.create(
                ab_id=f"{4000 + i}",
                ab_name=f"Regular Export {i}",
                catalog_num=f"REG{i:03d}",
                vendor=vendor,
                status=STATUS.CURATED
            )
        
        with patch('api.services.filesystem_service.check_if_file_does_not_exist_and_recent') as mock_file_check:
            mock_file_check.return_value = True
            with patch('api.services.export_service.generate_antibodies_csv_file'):
                response = self.client.get("/antibodies/export")
                # Should redirect to static file
                self.assertEqual(response.status_code, 302)
                self.assertTrue(response.headers['Location'].endswith('.csv'))

    def test_export_generates_valid_csv(self):
        """Test that export generates valid CSV content"""
        vendor = Vendor.objects.create(vendor="CSV Vendor", commercial_type="commercial")
        ab = Antibody.objects.create(
            ab_id="5001",
            ab_name="CSV Test Antibody",
            catalog_num="CSV001",
            vendor=vendor,
            status=STATUS.CURATED
        )
        
        # Test POST endpoint which returns CSV content
        response = self.client.post("/antibodies/export")
        csv_content = response.json()
        
        # Verify CSV structure
        lines = csv_content.strip().split('\n')
        self.assertGreater(len(lines), 1)
        
        # Check that data line contains antibody info
        data_found = False
        for line in lines[1:]:  # Skip header
            if 'AB_5001' in line or '5001' in line:
                data_found = True
                break
        self.assertTrue(data_found, "Antibody data should be in exported CSV")

    def test_export_with_special_characters(self):
        """Test export handles special characters correctly"""
        vendor = Vendor.objects.create(vendor="Special Vendor", commercial_type="commercial")
        ab = Antibody.objects.create(
            ab_id="6001",
            ab_name='Anti-IL-8 "Special" (Clone: #123)',
            catalog_num="SPEC001",
            vendor=vendor,
            comments="Contains, commas, and \"quotes\"",
            status=STATUS.CURATED
        )
        
        response = self.client.post("/antibodies/export")
        csv_content = response.json()
        
        # CSV should properly escape special characters
        self.assertIsInstance(csv_content, str)
        self.assertGreater(len(csv_content), 0)

    @patch('api.services.user_service.check_if_user_is_admin')
    def test_export_admin_invalid_status(self, mock_check_admin):
        """Test admin export with invalid status parameter"""
        mock_check_admin.return_value = True
        
        response = self.admin_client.get("/antibodies/export/admin?status=invalid_status")
        self.assertEqual(response.status_code, 400)

    def test_export_requires_authentication(self):
        """Test that export endpoints require authentication"""
        from .utils import AnonymousTestClient
        anon_user = User.objects.create_user(username='anon')
        anon_client = AnonymousTestClient(antibody.router, anon_user)
        
        # GET export should require auth
        response = anon_client.get("/antibodies/export")
        self.assertEqual(response.status_code, 401)
        
        # POST export should require auth
        response = anon_client.post("/antibodies/export")
        self.assertEqual(response.status_code, 401)

    def test_export_caching(self):
        """Test that export uses file caching appropriately"""
        vendor = Vendor.objects.create(vendor="Cache Vendor", commercial_type="commercial")
        Antibody.objects.create(
            ab_id="7001",
            ab_name="Cache Test",
            vendor=vendor,
            status=STATUS.CURATED
        )
        
        with patch('api.services.filesystem_service.check_if_file_does_not_exist_and_recent') as mock_file_check:
            # First call - file doesn't exist
            mock_file_check.return_value = True
            with patch('api.services.export_service.generate_antibodies_csv_file') as mock_generate:
                response = self.client.get("/antibodies/export")
                self.assertEqual(response.status_code, 302)
                # Should call generate function
                mock_generate.assert_called_once()
            
            # Second call - file exists and is recent
            mock_file_check.return_value = False
            with patch('api.services.export_service.generate_antibodies_csv_file') as mock_generate:
                response = self.client.get("/antibodies/export")
                self.assertEqual(response.status_code, 302)
                # Should NOT call generate function
                mock_generate.assert_not_called()
