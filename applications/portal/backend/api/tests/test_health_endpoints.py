"""
Tests for test/health check endpoints (ping, live, ready)
"""
from django.test import TestCase
from django.contrib.auth.models import User

from api.routers import test as test_router
from .utils import LoggedinTestClient, AnonymousTestClient


class HealthCheckEndpointsTestCase(TestCase):
    def setUp(self):
        """Set up test clients"""
        self.test_user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        # Create test clients for both authenticated and anonymous users
        self.client = LoggedinTestClient(test_router.router, self.test_user)
        self.anon_client = AnonymousTestClient(test_router.router, User.objects.create_user(username='anon'))

    def test_ping_endpoint(self):
        """Test GET /ping endpoint"""
        response = self.client.get("/ping")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), "Ping!")
        
        # Test with anonymous user
        response = self.anon_client.get("/ping")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), "Ping!")

    def test_live_endpoint(self):
        """Test GET /live endpoint"""
        response = self.client.get("/live")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), "I'm alive!")
        
        # Test with anonymous user
        response = self.anon_client.get("/live")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), "I'm alive!")

    def test_ready_endpoint(self):
        """Test GET /ready endpoint"""
        response = self.client.get("/ready")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), "I'm READY!")
        
        # Test with anonymous user
        response = self.anon_client.get("/ready")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), "I'm READY!")

    def test_all_health_endpoints_accessibility(self):
        """Verify all health check endpoints are accessible without authentication"""
        endpoints = ["/ping", "/live", "/ready"]
        
        for endpoint in endpoints:
            with self.subTest(endpoint=endpoint):
                response = self.anon_client.get(endpoint)
                self.assertEqual(response.status_code, 200)
                self.assertIsNotNone(response.json())
