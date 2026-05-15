"""
Tests for general API endpoints (datainfo, partners)
"""
from django.test import TestCase
from django.contrib.auth.models import User
from django.utils.timezone import now
import dateutil.relativedelta

from api.models import Antibody, STATUS, Partner
from api.routers import general
from .utils import LoggedinTestClient, AnonymousTestClient
from cloudharness_django.models import Member


class GeneralEndpointsTestCase(TestCase):
    def setUp(self):
        """Set up test user and client"""
        self.test_user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        # Create test clients for both authenticated and anonymous users
        self.client = LoggedinTestClient(general.router, self.test_user)
        self.anon_client = AnonymousTestClient(general.router, User.objects.create_user(username='anon'))
        
        self.user_id = "test-user-id-123"
        Member.objects.create(kc_id=self.user_id, user=self.test_user)

    def test_get_datainfo(self):
        """Test GET /datainfo endpoint"""
        # Create some test antibodies with curated status
        for i in range(5):
            ab = Antibody.objects.create(
                ab_id=f"{1000 + i}",
                ab_name=f"Test Antibody {i}",
                status=STATUS.CURATED
            )
            # Set curate_time for some antibodies
            if i < 3:
                ab.curate_time = now()
                ab.save()
        
        # Create some non-curated antibodies (should not be counted)
        for i in range(3):
            Antibody.objects.create(
                ab_id=f"{2000 + i}",
                ab_name=f"Queue Antibody {i}",
                status=STATUS.QUEUE
            )
        
        # Test with authenticated user
        response = self.client.get("/datainfo")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        
        self.assertIn('total', data)
        self.assertIn('lastupdate', data)
        self.assertEqual(data['total'], 5)  # Only curated antibodies
        
        # Test with anonymous user
        response = self.anon_client.get("/datainfo")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['total'], 5)

    def test_get_datainfo_empty_database(self):
        """Test GET /datainfo with no antibodies"""
        response = self.client.get("/datainfo")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        
        self.assertEqual(data['total'], 0)
        self.assertIsNotNone(data['lastupdate'])

    def test_get_partners(self):
        """Test GET /partners endpoint"""
        # Create test partners
        partner1 = Partner.objects.create(
            name="Partner One",
            url="https://partner1.example.com",
            image="partners/partner1.png"
        )
        
        partner2 = Partner.objects.create(
            name="Partner Two",
            url="https://partner2.example.com",
            image="partners/partner2.png"
        )
        
        partner3 = Partner.objects.create(
            name="Partner Three",
            url="https://partner3.example.com"
            # No image
        )
        
        # Test with authenticated user
        response = self.client.get("/partners")
        self.assertEqual(response.status_code, 200)
        partners = response.json()
        
        self.assertEqual(len(partners), 3)
        
        # Check first partner
        partner1_data = next((p for p in partners if p['name'] == 'Partner One'), None)
        self.assertIsNotNone(partner1_data)
        self.assertEqual(partner1_data['url'], 'https://partner1.example.com')
        self.assertIn('/media/partners/partner1.png', partner1_data['image'])
        
        # Check partner without image
        partner3_data = next((p for p in partners if p['name'] == 'Partner Three'), None)
        self.assertIsNotNone(partner3_data)
        self.assertIsNone(partner3_data['image'])
        
        # Test with anonymous user
        response = self.anon_client.get("/partners")
        self.assertEqual(response.status_code, 200)
        partners = response.json()
        self.assertEqual(len(partners), 3)

    def test_get_partners_empty(self):
        """Test GET /partners with no partners in database"""
        response = self.client.get("/partners")
        self.assertEqual(response.status_code, 200)
        partners = response.json()
        self.assertEqual(len(partners), 0)

    def test_datainfo_lastupdate_calculation(self):
        """Test that lastupdate reflects most recent curated antibody"""
        # Create older antibody
        old_ab = Antibody.objects.create(
            ab_id="1001",
            ab_name="Old Antibody",
            status=STATUS.CURATED
        )
        old_ab.curate_time = now() - dateutil.relativedelta.relativedelta(months=1)
        old_ab.save()
        
        # Create newer antibody
        new_ab = Antibody.objects.create(
            ab_id="1002",
            ab_name="New Antibody",
            status=STATUS.CURATED
        )
        new_ab.curate_time = now()
        new_ab.save()
        
        response = self.client.get("/datainfo")
        data = response.json()
        
        # The lastupdate should be from the newest antibody
        self.assertEqual(data['lastupdate'], new_ab.curate_time.date().isoformat())
