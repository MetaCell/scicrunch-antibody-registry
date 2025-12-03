#!/usr/bin/env python
"""
Quick test to verify the URL visibility fix is working
"""
import os
import sys

# Setup Django BEFORE importing Django modules
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'portal.settings')
import django
django.setup()

from django.test import TestCase
from django.contrib.auth.models import User
from unittest.mock import patch

from api.models import Antibody, Vendor, VendorDomain, VendorSynonym, Specie, STATUS
from api.schemas import AddAntibody, AntibodyStatusEnum as Status, CommercialTypeEnum as CommercialType, ClonalityEnum as Clonality
from api.routers.antibody import router
from api.tests.utils import LoggedinTestClient
from cloudharness_django.models import Member

# Test data
example_ab = {
    "clonality": "cocktail",
    "epitope": "OTTHUMP00000018992",
    "comments": "comment is free text",
    "url": "https://www.bdbiosciences.com/en-it/products/reagents/flow-cytometry-reagents/clinical-discovery-research/single-color-antibodies-ruo-gmp/pe-mouse-anti-human-il-8.340510",
    "abName": "BD FastImmune™ PE Mouse Anti-Human IL-8",
    "abTarget": "LRKK2",
    "catalogNum": "N176A/35",
    "cloneId": "N176A/35",
    "commercialType": "commercial",
    "definingCitation": "1000",
    "productConjugate": "string",
    "productForm": "string",
    "productIsotype": "string",
    "sourceOrganism": "mouse",
    "targetSpecies": ["mouse", "human"],
    "uniprotId": "uuiid",
    "vendorName": "My vendorname",
    "applications": "ELISA, IHC, WB".split(", "),
    "kitContents": "Sheep polyclonal anti-FSH antibody labeled with acridinium ester. Mouse monoclonal anti-FSH antibody covalently coupled to paramagnetic particles.",
}

def test_url_visibility():
    """Test that URL is visible to creator user"""
    print("Testing URL visibility fix...")
    
    # Create a test user
    test_user = User.objects.create_user(
        username='testuser',
        email='test@example.com',
        password='testpass123'
    )
    
    # Create test client
    client = LoggedinTestClient(router, test_user)
    user_id = "66a9dd54-2214-4ed7-b4f8-daa5bf3c9a79"
    Member.objects.create(kc_id=user_id, user=test_user)
    
    # Mock the mapping utils function for schema serialization
    with patch('api.mappers.mapping_utils.get_current_user_id') as mock_get_user_id:
        mock_get_user_id.return_value = user_id
        
        # Create antibody
        response = client.post("/antibodies", json=example_ab)
        print(f"Create response status: {response.status_code}")
        
        if response.status_code == 201:
            ab = response.json()
            print(f"Created antibody ID: {ab['abId']}")
            print(f"URL in response: {ab.get('url')}")
            
            # Test: URL should be visible to creator
            if ab.get('url') == example_ab['url']:
                print("✅ SUCCESS: URL is correctly visible to creator user")
                return True
            else:
                print(f"❌ FAIL: Expected URL '{example_ab['url']}', got '{ab.get('url')}'")
                return False
        else:
            print(f"❌ FAIL: Failed to create antibody, status: {response.status_code}")
            print(f"Response: {response.json() if hasattr(response, 'json') else response.content}")
            return False

if __name__ == "__main__":
    try:
        success = test_url_visibility()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)