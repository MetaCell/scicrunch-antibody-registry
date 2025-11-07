#!/usr/bin/env python
import os
import sys
import django

# Add the project directory to the path
sys.path.insert(0, '.')

# Set the Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'portal.settings')

# Setup Django
django.setup()

from django.test import TestCase, override_settings
from django.contrib.auth.models import User
from api.tests.utils import LoggedinTestClient
from api.api import api
from cloudharness_django.models import Member


class DebugTest(TestCase):
    def setUp(self):
        self.test_user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        # Create Django Ninja test client with authenticated user
        self.client = LoggedinTestClient(api, self.test_user)
        
        self.user_id = "66a9dd54-2214-4ed7-b4f8-daa5bf3c9a79"
        Member.objects.create(kc_id=self.user_id, user=self.test_user)

    def test_debug_endpoints(self):
        print("Testing available endpoints...")
        
        # Test GET endpoint that should work
        print("Testing GET /species:")
        response = self.client.get("/species")
        print(f"  Status: {response.status_code}")
        
        # Test POST endpoint that's failing
        print("Testing POST /antibodies/search:")
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
            "isUserScope": True,
        }
        
        response = self.client.post("/antibodies/search", json=filter_data)
        print(f"  Status: {response.status_code}")
        
        if response.status_code != 200:
            print(f"  Content: {response.content}")
            print(f"  Headers: {dict(response.headers)}")
        
        # Let's also check what methods are allowed
        print("Testing OPTIONS /antibodies/search:")
        response = self.client.options("/antibodies/search")
        print(f"  Status: {response.status_code}")
        if 'allow' in response.headers:
            print(f"  Allowed methods: {response.headers['allow']}")


if __name__ == "__main__":
    test = DebugTest()
    test.setUp() 
    test.test_debug_endpoints()