from django.test import TestCase
from django.contrib.auth.models import User
from unittest.mock import patch
from api.models import Vendor, Antibody, VendorDomain, VendorSynonym, Specie, STATUS
from api.utilities.exceptions import DuplicatedAntibody
from api.schemas import (
    AddAntibody,
    AntibodyStatusEnum as Status,
    CommercialTypeEnum as CommercialType,
    ClonalityEnum as Clonality,
    UpdateAntibody,
)
from api.routers import antibody, search
from .data.test_data import example_ab2, example_ab
from .utils import LoggedinTestClient
from cloudharness_django.models import Member

class AntibodiesTestCase(TestCase):
    def setUp(self):
        """Set up test user and client"""
        print("DEBUG: setUp started")
        # Create a test user
        self.test_user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        print("DEBUG: User created")
        
        # Create Django Ninja test client with authenticated user - create combined router
        print("DEBUG: Creating LoggedinTestClient")
        from ninja import NinjaAPI
        import uuid
        combined_api = NinjaAPI(title="Test API", urls_namespace=f"test_{uuid.uuid4().hex[:8]}")
        # Detach routers from their existing API to avoid conflicts
        antibody.router.api = None
        search.router.api = None
        combined_api.add_router("", antibody.router)
        combined_api.add_router("", search.router)
        # Add exception handlers
        from api.helpers.response_helpers import add_exception_handlers
        add_exception_handlers(combined_api)
        self.client = LoggedinTestClient(combined_api, self.test_user)
        print("DEBUG: LoggedinTestClient created")
        self.user_id = "66a9dd54-2214-4ed7-b4f8-daa5bf3c9a79"
        Member.objects.create(kc_id=self.user_id, user=self.test_user)
        
        # Mock the function in mapping_utils which is used by schema serialization
        print("DEBUG: Setting up mocks")
        self.get_user_id_mapping_patcher = patch('api.mappers.mapping_utils.get_current_user_id')
        self.mock_get_user_id_mapping = self.get_user_id_mapping_patcher.start()
        self.mock_get_user_id_mapping.return_value = self.user_id
        print("DEBUG: setUp complete")
    
    def tearDown(self):
        """Clean up patches"""
        self.get_user_id_mapping_patcher.stop()

    def test_create(self):
        """Test creating antibodies via Django Ninja API"""
        # Create antibody via API
        print("DEBUG: About to call client.post")
        response = self.client.post("/antibodies", json=example_ab)
        print(f"DEBUG: Got response with status {response.status_code}")
        self.assertEqual(response.status_code, 201)
        ab = response.json()
        
        self.assertEqual(ab['clonality'], Clonality.cocktail.value)
        self.assertEqual(ab['commercialType'], CommercialType.commercial.value)
        self.assertIsNotNone(ab['vendorId'])
        self.assertEqual(ab['vendorName'], "My vendorname")
        self.assertEqual(ab['status'], Status.QUEUE.value)
        
        # Curate vendor domains
        self.curate_vendor_domains_for_antibody(ab['abId'])
        
        # Get antibody via API
        response = self.client.get(f"/antibodies/{ab['abId']}")
        self.assertEqual(response.status_code, 200)
        ab_list = response.json()
        
        
        ab = ab_list[0] if isinstance(ab_list, list) else ab_list
        
        self.assertTrue("www.bdbiosciences.com" in ab['vendorUrl'])
        
        # Test URL visibility - should be shown to creator user
        self.assertEqual(ab.get('url'), example_ab['url'])
        
        # Set show_link to True
        antibody1 = Antibody.objects.get(ix=ab['ix'])
        antibody1.show_link = True
        antibody1.save()
        
        response = self.client.get(f"/antibodies/{ab['abId']}")
        ab1_with_url = response.json()[0]
        example_ab_url = example_ab['url']
        self.assertEqual(ab1_with_url['url'], example_ab_url)
        
        # Test with creator user ID
        example_ab3 = example_ab.copy()
        example_ab3['catalogNum'] = "N176A/786"
        response = self.client.post("/antibodies", json=example_ab3)
        ab_with_token_user = response.json()
        self.assertEqual(ab_with_token_user['url'], example_ab_url)
        
        self.assertIsNotNone(ab['insertTime'])
        self.assertIsNone(ab.get('curateTime'))
        self.assertEqual(ab['sourceOrganism'], "mouse")
        self.assertEqual(len(ab['targetSpecies']), 2)
        
        # Create another antibody with different catalog number
        new_ant = example_ab.copy()
        new_ant['catalogNum'] = "N176A/36"
        new_ant['abName'] = "Another antibody"
        new_ant['url'] = "https://www.ab.com/My-antibody"
        
        response = self.client.post("/antibodies", json=new_ant)
        ab2 = response.json()
        
        self.assertNotEqual(ab['abId'], ab2['abId'])
        self.assertEqual(ab['vendorName'], ab2['vendorName'])
        
        domains = VendorDomain.objects.filter(vendor__id=ab2['vendorId'])
        self.assertEqual(len(domains), 2)
        
        # Test get all antibodies (should return 0 as they're not curated)
        response = self.client.get("/antibodies")
        abs_response = response.json()
        self.assertEqual(abs_response['page'], 1)
        self.assertEqual(len(abs_response['items']), 0)
        
        # Test get user antibodies
        response = self.client.get("/antibodies/user")
        user_abs = response.json()
        self.assertEqual(user_abs['page'], 1)
        self.assertEqual(len(user_abs['items']), 3)  # 3 antibodies created by this user
        abget = user_abs['items'][0]
        self.assertEqual(len(abget['targetSpecies']), 2)
        
        # Get antibody with status QUEUE
        response = self.client.get(f"/antibodies/{ab['abId']}")
        ab3 = response.json()[0]
        self.assertEqual(ab1_with_url['url'], ab3['url'])
        
        # Curate first antibody
        a = Antibody.objects.get(ab_id=ab['abId'])
        a.status = STATUS.CURATED
        a.save()
        self.assertIsNotNone(a.curate_time)
        
        # Now should appear in public list
        response = self.client.get("/antibodies")
        abs_response = response.json()
        self.assertEqual(len(abs_response['items']), 1)
        
        # Curate second antibody
        a = Antibody.objects.get(ab_id=ab2['abId'])
        a.status = STATUS.CURATED
        a.save()
        
        # Test duplicate detection
        duplicated = example_ab.copy()
        response = self.client.post("/antibodies", json=duplicated)
        # Should return error or handle duplicate
        self.assertIn(response.status_code, [400, 409])  # Bad request or conflict
        
        self.assertEqual(VendorDomain.objects.all().count(), 2)
        self.assertEqual(Vendor.objects.all().count(), 1)
        
        # Test with entrez_id and uniprot_id
        response = self.client.post("/antibodies", json=example_ab2)
        ab = response.json()
        
        a = Antibody.objects.get(ab_id=ab['abId'])
        a.status = STATUS.CURATED
        a.entrez_id = "entrez"
        a.uniprot_id = "uniprot"
        a.show_link = True
        a.save()
        
        response = self.client.get(f"/antibodies/{ab['abId']}")
        ab = response.json()[0]
        self.assertEqual(ab['abTargetEntrezId'], "entrez")
        self.assertEqual(ab['abTargetUniprotId'], "uniprot")
        self.assertIsNotNone(ab['ix'])
        self.assertIsNotNone(ab.get('showLink'))
        
        # Test get by accession
        response = self.client.get(f"/antibodies/user/{ab['accession']}")
        ab_by_accession = response.json()
        self.assertEqual(ab_by_accession['abId'], ab['abId'])
        self.assertEqual(ab_by_accession['accession'], ab['accession'])
        self.assertEqual(ab_by_accession['vendorName'], ab['vendorName'])
        
        return ab

    def test_fts(self):
        """Test full-text search via Django Ninja API"""
        ab = self.test_create()
        
        # Ensure search view is refreshed for testing
        from api.repositories.maintainance import refresh_search_view
        refresh_search_view()
        
        # Search by catalog number - should find 2 results
        response = self.client.get("/fts-antibodies?q=N176A")
        result = response.json()
        self.assertEqual(len(result['items']), 2)
        
        response = self.client.get("/fts-antibodies?q=N176A 35")
        self.assertEqual(len(response.json()['items']), 1)
        
        response = self.client.get("/fts-antibodies?q=N176A|35")
        self.assertEqual(len(response.json()['items']), 1)
        
        response = self.client.get("/fts-antibodies?q=N17")
        self.assertEqual(len(response.json()['items']), 0)
        
        # Update catalog numbers
        a = Antibody.objects.get(ab_id=ab['abId'])
        a.catalog_num = "N0304-AB635P-L"
        a.cat_alt = "N0304-AB635P-S"
        a.save()
        
        response = self.client.get("/fts-antibodies?q=N0304-AB635P-L")
        self.assertEqual(len(response.json()['items']), 1)
        
        response = self.client.get("/fts-antibodies?q=N0304AB635PL")
        self.assertEqual(len(response.json()['items']), 1)
        
        response = self.client.get("/fts-antibodies?q=N0304-AB635P-S")
        self.assertEqual(len(response.json()['items']), 1)
        
        response = self.client.get("/fts-antibodies?q=635P-L")
        self.assertEqual(len(response.json()['items']), 1)
        
        response = self.client.get("/fts-antibodies?q=N0304-AB635P-X")
        self.assertEqual(len(response.json()['items']), 0)
        
        # Search in name
        response = self.client.get("/fts-antibodies?q=FastImmune")
        self.assertEqual(len(response.json()['items']), 1)
        
        response = self.client.get("/fts-antibodies?q=fastImmune")
        self.assertEqual(len(response.json()['items']), 1, "Search must be case insensitive")
        
        response = self.client.get("/fts-antibodies?q=FastImmune PE Mouse")
        self.assertEqual(len(response.json()['items']), 1)
        
        response = self.client.get("/fts-antibodies?q=BD FastImmune™ PE Mouse Anti-Human IL-8")
        self.assertEqual(len(response.json()['items']), 1)
        
        response = self.client.get("/fts-antibodies?q=BD FastImmune™ PE Mouse (Anti-Human) IL-8")
        self.assertEqual(len(response.json()['items']), 1, "Must ignore special characters")
        
        response = self.client.get("/fts-antibodies?q=Sheep polyclonal anti-FSH antibody labeled with acridinium ester")
        self.assertEqual(len(response.json()['items']), 2, "Search in kit contents")
        
        response = self.client.get("/fts-antibodies?q=External validation DATA SET is released testing")
        self.assertEqual(len(response.json()['items']), 1, "Search in comments")
        
        response = self.client.get("/fts-antibodies?q=vendorname")
        self.assertEqual(len(response.json()['items']), 2)
        
        response = self.client.get("/fts-antibodies?q=Andrew Dingwall")
        self.assertEqual(len(response.json()['items']), 1)
        
        response = self.client.get("/fts-antibodies?q=rabbit")
        self.assertEqual(len(response.json()['items']), 1, "Search in source organism")
        
        response = self.client.get("/fts-antibodies?q=Rabbit")
        self.assertEqual(len(response.json()['items']), 1, "case insensitive search")
        
        # Should also search for accession when searching with AB_
        ab2 = Antibody.objects.create(
            ab_id="1234567",
            accession="12345689",
            ab_name="ab2",
        )
        ab2.status = STATUS.CURATED
        ab2.save()
        
        # Refresh search view to include the new antibody
        refresh_search_view()
        
        response = self.client.get("/fts-antibodies?q=AB_1234567")
        self.assertEqual(len(response.json()['items']), 1)
        
        response = self.client.get("/fts-antibodies?q=AB_12345689")
        self.assertEqual(len(response.json()['items']), 1)  # search into accession

    def test_update(self):
        """Test updating antibodies via Django Ninja API"""
        user_id = self.user_id
        new_name = "My updated abName"
        
        # Create antibody
        response = self.client.post("/antibodies", json=example_ab)
        ab = response.json()
        
        # Get user antibodies
        response = self.client.get("/antibodies/user?page=1&size=1")
        user_antibodies = response.json()
        ab_to_update = user_antibodies['items'][0]
        
        self.assertNotEqual(ab['abName'], new_name)
        self.assertEqual(ab['abId'], ab_to_update['abId'])
        
        # Update antibody
        ab_update_example = dict(example_ab)
        ab_update_example["abName"] = new_name
        
        response = self.client.put(
            f"/antibodies/user/{ab_to_update['accession']}", 
            json=ab_update_example
        )
        self.assertEqual(response.status_code, 202)
        updated_ab = response.json()
        self.assertEqual(updated_ab['abName'], new_name)
        
        # Test that vendor name is not included in UpdateAntibody schema (field is ignored)
        ab_update_example["vendorName"] = "Vendor Update Test"
        response = self.client.put(
            f"/antibodies/user/{ab_to_update['accession']}", 
            json=ab_update_example
        )
        self.assertEqual(response.status_code, 202)  # Should succeed, but vendor name is ignored
        
        # Verify vendor name wasn't actually updated
        updated_response = self.client.get(f"/antibodies/user/{ab_to_update['accession']}")
        updated_ab = updated_response.json()
        self.assertEqual(updated_ab['vendorName'], ab_to_update['vendorName'])  # Should remain unchanged
        
        # Test species handling
        dao = Antibody.objects.get(ab_id=ab['abId'])
        dao.species.set([])
        dao.save()
        self.assertEqual(dao.species.count(), 0)
        self.assertEqual(len(dao.target_species_raw), 0)
        
        dao.target_species_raw = "mouse"
        dao.species.add(Specie.objects.get(name="human"))
        dao.save()
        self.assertEqual(dao.species.count(), 2)
        self.assertIn("human", dao.target_species_raw)
        self.assertIn("mouse", dao.target_species_raw)
        
        dao.target_species_raw = "mouse,human,rat,human,mouse"
        dao.save()
        self.assertEqual(dao.species.count(), 3)

    @staticmethod
    def curate_test_antibody_data(ab_id):
        a: Antibody = Antibody.objects.get(ab_id=ab_id)
        a.status = STATUS.CURATED
        a.save()

    @staticmethod
    def curate_vendor_domains_for_antibody(ab_id):
        a: Antibody = Antibody.objects.get(ab_id=ab_id)
        for domain in a.vendor.vendordomain_set.all():
            domain.status = STATUS.CURATED
            domain.save()

    def test_antibody_create__vendors(self):
        """
        Test vendor recognition logic via Django Ninja API
        If a new antibody is submitted with some vendor name and URL
        should be treated with following rules:
        - If both domain and vendor name are not recognized,
            a new vendor is created and the new domain is attached to the vendor.
        - If both domain and vendor name are recognized,
            the domain is prioritized. And vendor name is added as a synonym.
        - If the domain is not recognized but vendor name is recognized,
            the new domain is attached to the vendor recognized.
        - If domain is recognized and vendor name is not recognized,
            we add a vendor synonym
        """
        # Vendor recognition priority is domain > vendor name
        V1_D1 = "www.bdbiosciences.com"
        V1_N1 = example_ab["vendorName"]
        V2_D1 = "www.v2d1.com"
        V2_N1 = "v2n1"
        V2_D2 = "www.v2d2.com"
        V3_D1 = "www.v3d1.com"
        V3_N1 = "v3n1"
        V1_N2 = "v1n2"

        # Expect 3 vendors to be created

        ### first antibody ###
        response = self.client.post("/antibodies", json=example_ab)
        ab = response.json()
        
        self.assertEqual(ab['vendorName'], V1_N1)
        self.assertTrue(all(v.status == STATUS.QUEUE for v in VendorDomain.objects.all()))
        self.assertEqual(len(ab.get('vendorUrl', [])), 0, "Vendor URL should not be shown as it's not curated yet")
        
        self.curate_test_antibody_data(ab['abId'])
        self.curate_vendor_domains_for_antibody(ab['abId'])
        
        response = self.client.get(f"/antibodies/{ab['abId']}")
        ab = response.json()[0]  # returns a list - get the first one

        self.assertIn(V1_D1, ab['vendorUrl'])

        # Number of vendors 1 and vendor domain 1
        self.assertEqual(VendorDomain.objects.count(), 1)
        self.assertEqual(Vendor.objects.count(), 1)

        ### both domain and vendor name are not recognized  ###
        # will create a new vendor since both vendor name and url are different
        modified_example_ab = example_ab.copy()
        modified_example_ab["vendorName"] = V2_N1
        modified_example_ab["url"] = "https://" + V2_D1 + "/test"
        modified_example_ab["catalogNum"] = "N176AB_23/35_SD_WEER"
        
        response = self.client.post("/antibodies", json=modified_example_ab)
        ab2 = response.json()

        self.curate_test_antibody_data(ab2['abId'])
        self.curate_vendor_domains_for_antibody(ab2['abId'])
        
        response = self.client.get(f"/antibodies/{ab2['abId']}")
        ab2 = response.json()[0]

        self.assertEqual(ab2['vendorName'], V2_N1)
        self.assertNotEqual(ab2['vendorId'], ab['vendorId'])
        self.assertEqual(ab2['vendorUrl'], [V2_D1])

        # Number of vendors 2, vendor domain 2
        self.assertEqual(VendorDomain.objects.count(), 2)
        self.assertEqual(Vendor.objects.count(), 2)

        # Before the vendor synonym is saved in the operation below, check should be empty
        self.assertEqual(VendorSynonym.objects.count(), 0)

        # Both domain and vendor name are recognized ->
        # domain is prioritized and vendor name is added as synonym
        modified_example_ab = example_ab.copy()
        modified_example_ab["url"] = "https://" + V1_D1 + "/test"
        modified_example_ab["vendorName"] = V2_N1
        modified_example_ab["catalogNum"] = "N176AB_23/35_SD"
        
        response = self.client.post("/antibodies", json=modified_example_ab)
        ab3 = response.json()
        
        self.curate_test_antibody_data(ab3['abId'])
        
        response = self.client.get(f"/antibodies/{ab3['abId']}")
        ab3 = response.json()[0]
        
        self.assertEqual(ab3['vendorName'], V1_N1)
        self.assertEqual(ab3['vendorId'], ab['vendorId'])
        self.assertEqual(ab3['vendorUrl'], [V1_D1])

        # Number of vendors 2, vendor domain 2
        self.assertEqual(VendorDomain.objects.count(), 2)
        self.assertEqual(Vendor.objects.count(), 2)

        # the above should add a new vendor synonym
        self.assertEqual(VendorSynonym.objects.count(), 1)

        ### the domain is not recognized but vendor name is recognized. ###
        modified_example_ab = example_ab.copy()
        modified_example_ab["url"] = "https://" + V2_D2
        modified_example_ab["vendorName"] = V2_N1
        modified_example_ab["catalogNum"] = "N176AB_23/35_SD"
        
        response = self.client.post("/antibodies", json=modified_example_ab)
        ab4 = response.json()
        
        self.curate_test_antibody_data(ab4['abId'])
        self.curate_vendor_domains_for_antibody(ab4['abId'])
        
        response = self.client.get(f"/antibodies/{ab4['abId']}")
        ab4 = response.json()[0]

        self.assertEqual(ab4['vendorName'], ab2['vendorName'])
        self.assertEqual(set(ab4['vendorUrl']), set([V2_D1, V2_D2]))
        self.assertEqual(ab4['vendorId'], ab2['vendorId'])

        # Number of vendors 2, vendor domain 3 - the new url is attached to the vendor recognized
        self.assertEqual(set(ab4['vendorUrl']), set([V2_D1, V2_D2]))
        self.assertEqual(VendorDomain.objects.count(), 3)
        self.assertEqual(Vendor.objects.count(), 2)

        ### Both domain and vendor name are not recognized ###
        modified_example_ab = example_ab.copy()
        modified_example_ab["url"] = "https://" + V3_D1
        modified_example_ab["vendorName"] = V3_N1
        modified_example_ab["catalogNum"] = "N176AB_23/35_SD_456"
        
        response = self.client.post("/antibodies", json=modified_example_ab)
        ab5 = response.json()
        
        self.curate_test_antibody_data(ab5['abId'])
        
        response = self.client.get(f"/antibodies/{ab5['abId']}")
        ab5 = response.json()[0]

        # this creates a new vendor domain and vendor
        # Number of vendors 3, vendor domain 4
        self.assertEqual(VendorDomain.objects.count(), 4)
        self.assertEqual(Vendor.objects.count(), 3)

        ### domain is recognized but vendor name is not recognized ###
        # should also create a new vendor synonym
        modified_example_ab = example_ab.copy()
        modified_example_ab["url"] = "https://" + V1_D1 + "/_test"
        modified_example_ab["vendorName"] = V1_N2
        modified_example_ab["catalogNum"] = "N176AB_23/35_IPL"
        
        response = self.client.post("/antibodies", json=modified_example_ab)
        ab6 = response.json()
        
        self.curate_test_antibody_data(ab6['abId'])
        
        response = self.client.get(f"/antibodies/{ab6['abId']}")
        ab6 = response.json()[0]

        self.assertEqual(ab6['vendorName'], ab['vendorName'])
        self.assertEqual(ab6['vendorId'], ab['vendorId'])
        self.assertEqual(ab6['vendorUrl'], ab['vendorUrl'])

        # A new vendor synonym is added, since vendor name is not recognized
        self.assertEqual(VendorSynonym.objects.count(), 2)
        self.assertEqual(Vendor.objects.count(), 3)
