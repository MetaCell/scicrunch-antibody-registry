from django.test import TestCase
from api.services.antibody_service import *
from api.services.search_service import fts_antibodies
from api.models import Vendor, VendorDomain, VendorSynonym
from api.repositories.maintainance import refresh_search_view

from openapi.models import (
    AddAntibody as AddAntibodyDTO,
    Status,
    CommercialType,
    Clonality,
    UpdateAntibody,
    AddAntibody,
)

from ..models import Vendor, Antibody, VendorDomain, Specie
from .data.test_data import example_ab2, example_ab
from cloudharness.middleware import set_authentication_token, get_authentication_token
from api.services.user_service import get_current_user_id

token = "eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICJJUHJQcnZBanBrZ19HQlVUSVN5YVBoaXRMeUtVNDlQUGJRUTlPaWNBWEtzIn0.eyJleHAiOjE3MTAyMzg2MDAsImlhdCI6MTcxMDIyNzgwMCwiYXV0aF90aW1lIjoxNzEwMjI3ODAwLCJqdGkiOiIxZTFkMjRmMy0zMTU3LTRhNzEtOGI4Ny0yNzZhZjBkMGFjMTUiLCJpc3MiOiJodHRwczovL2FjY291bnRzLmFyZWcuZGV2Lm1ldGFjZWxsLnVzL2F1dGgvcmVhbG1zL2FyZWciLCJhdWQiOlsid2ViLWNsaWVudCIsImFjY291bnQiXSwic3ViIjoiNjZhOWRkNTQtMjIxNC00ZWQ3LWI0ZjgtZGFhNWJmM2M5YTc5IiwidHlwIjoiQmVhcmVyIiwiYXpwIjoid2ViLWNsaWVudCIsInNlc3Npb25fc3RhdGUiOiI1MzMyNDQ5MS0zNmY4LTRlODctOGE5YS0yZTIyODc3YmQxMDciLCJhY3IiOiIxIiwiYWxsb3dlZC1vcmlnaW5zIjpbIioiXSwicmVhbG1fYWNjZXNzIjp7InJvbGVzIjpbImFkbWluaXN0cmF0b3IiLCJkZWZhdWx0LXJvbGVzLWFyZWciXX0sInJlc291cmNlX2FjY2VzcyI6eyJhY2NvdW50Ijp7InJvbGVzIjpbIm1hbmFnZS1hY2NvdW50IiwibWFuYWdlLWFjY291bnQtbGlua3MiLCJ2aWV3LXByb2ZpbGUiXX19LCJzY29wZSI6Im9wZW5pZCBwcm9maWxlIGFkbWluaXN0cmF0b3Itc2NvcGUgZW1haWwiLCJzaWQiOiI1MzMyNDQ5MS0zNmY4LTRlODctOGE5YS0yZTIyODc3YmQxMDciLCJlbWFpbF92ZXJpZmllZCI6ZmFsc2UsIm5hbWUiOiJGaWxpcHBvIExlZGRhIiwicHJlZmVycmVkX3VzZXJuYW1lIjoiYSIsImdpdmVuX25hbWUiOiJGaWxpcHBvIiwiZmFtaWx5X25hbWUiOiJMZWRkYSIsImVtYWlsIjoiYUBhYS5pdCJ9.RShiiCZPEwz2IxEQqU2TBB1F6NQIOMfcrVU99eMSlXEahb38VegqUyIqUfoQUrQAHqnyysR67HeBuCq2SNh9ctxpAiEpFq7LAkqpEIQfByvdyDsBArT0jeWd6DuQ91_7PAdSPWqFEr-uFo9476NQZecrIuXCaNC3rrHbPb6GZKwT6gUMu_sCYAawT8jA_V9rpfgedM5PuqJHTp40of-ZDchD7Cc2NTIE2RopgkKifxtRRjQ9wwudz0hxKjVb9E9GCtkaA-MjDdEeVxnSgTu2p8Y9EaPOoZKt-zt0XTjRT8otwx7yOzz1euhDVh1-1zBb7V3Lt-w4BW19draYkGWMzg"


class AntibodiesTestCase(TestCase):
    def setUp(self):
        if token:
            set_authentication_token(token)
            user = get_current_user_id()

    def test_create(self):
        ab = create_antibody(AddAntibodyDTO(**example_ab), "aaaa")
        self.assertEquals(ab.clonality, Clonality.cocktail)
        self.assertEquals(ab.commercialType, CommercialType.commercial)
        self.assertIsNotNone(ab.vendorId)
        self.assertEquals(ab.vendorName, "My vendorname")
        self.assertEquals(ab.status, Status.QUEUE)
        self.curate_vendor_domains_for_antibody(ab.abId)
        ab = get_antibody(ab.abId, status=STATUS.QUEUE)[0]

        self.assertTrue("www.bdbiosciences.com" in ab.vendorUrl)
        

        # current token user is different than the user that created the antibody and link is false
        # so the url should not be shown
        self.assertIsNone(ab.url)

        # if show_link is set to True, the url should be shown
        antibody1 = Antibody.objects.get(ix=ab.ix)
        antibody1.show_link = True
        antibody1.save()
        ab1_with_url = antibody_mapper.to_dto(antibody1)
        example_ab_url = example_ab['url']
        self.assertEquals(ab1_with_url.url, example_ab_url)

        # if userid is the creator of the antibody, the url should be shown - test with a new example
        userid = get_current_user_id()
        example_ab3 = example_ab.copy()
        example_ab3['catalogNum'] = "N176A/786"
        ab_with_token_user = create_antibody(AddAntibodyDTO(**example_ab3), userid)
        self.assertEquals(ab_with_token_user.url, example_ab_url)

        self.assertIsNotNone(ab.insertTime)

        assert ab.curateTime is None
        assert ab.sourceOrganism == "mouse"
        assert len(ab.targetSpecies) == 2


        new_ant = AddAntibodyDTO(**example_ab)
        new_ant.catalogNum = "N176A/36"
        new_ant.abName = "Another antibody"
        new_ant.url = (
            "https://www.ab.com/My-antibody"  # should add this domain to the vendor
        )
        ab2 = create_antibody(new_ant, "bbb")
        self.assertNotEqual(ab.abId, ab2.abId)
        self.assertEquals(ab.vendorName, ab2.vendorName)

        domains = VendorDomain.objects.filter(vendor__id=ab2.vendorId)
        self.assertEquals(len(domains), 2)

        abs = get_antibodies()
        assert abs.page == 1
        assert len(abs.items) == 0
        assert count() == 0
        user_abs = get_user_antibodies("aaaa")
        assert user_abs.page == 1
        assert len(user_abs.items) == 1
        abget = user_abs.items[0]
        assert len(abget.targetSpecies) == 2

        ab3 = get_antibody(ab.abId, status=STATUS.QUEUE)[0]
        assert ab1_with_url.url == ab3.url

        a: Antibody = Antibody.objects.get(ab_id=ab.abId)
        a.status = STATUS.CURATED
        a.save()
        assert a.curate_time

        abs = get_antibodies()
        assert len(abs.items) == 1

        assert count() == 1
        print(last_update())

        a: Antibody = Antibody.objects.get(ab_id=ab2.abId)
        a.status = STATUS.CURATED
        a.save()

        duplicated = AddAntibodyDTO(**example_ab)
        # duplicated.vendorName = "My vendor synonym" # should keep the same vendor and add a synonym
        da = create_antibody(duplicated, "bbb")

        assert da.accession != da.abId
        assert da.abId == ab.abId
        assert da.status == Status.QUEUE
        assert da.vendorId == ab.vendorId
        assert da.vendorName == "My vendorname"

        assert VendorDomain.objects.all().count() == 2
        assert Vendor.objects.all().count() == 1

        # Test search

        ab = create_antibody(AddAntibodyDTO(**example_ab2), "aaaa")
        a: Antibody = Antibody.objects.get(ab_id=ab.abId)
        a.status = STATUS.CURATED
        a.entrez_id = "entrez"
        a.uniprot_id = "uniprot"
        a.show_link = True
        a.save()

        ab = get_antibody(ab.abId)[0]
        assert ab.abTargetEntrezId == "entrez"
        assert ab.abTargetUniprotId == "uniprot"
        assert ab.ix
        assert ab.showLink is not None

        ab_by_accession = get_antibody_by_accession(ab.accession)
        assert ab_by_accession.abId == ab.abId
        assert ab_by_accession.accession == ab.accession
        assert ab_by_accession.vendorName == ab.vendorName
        return ab

    def test_fts(self):
        ab = self.test_create()
        # Search by catalog number
        self.assertEquals(len(fts_antibodies(search="N176A").items), 2)
        assert len(fts_antibodies(search="N176A 35").items) == 1
        assert len(fts_antibodies(search="N176A|35").items) == 1
        assert len(fts_antibodies(search="N176A|35").items) == 1
        assert len(fts_antibodies(search="N17").items) == 0

        assert len(fts_antibodies(search="N17").items) == 0

        a = Antibody.objects.get(ab_id=ab.abId)
        a.catalog_num = "N0304-AB635P-L"
        a.cat_alt = "N0304-AB635P-S"
        a.save()

        assert len(fts_antibodies(search="N0304-AB635P-L").items) == 1
        assert len(fts_antibodies(search="N0304AB635PL").items) == 1
        assert len(fts_antibodies(search="N0304-AB635P-S").items) == 1
        assert len(fts_antibodies(search="635P-L").items) == 1
        assert len(fts_antibodies(search="N0304-AB635P-X").items) == 0

        # # Search in name
        assert len(fts_antibodies(search="FastImmune").items) == 1
        assert len(fts_antibodies(search="fastImmune").items) == 1, "Search must be case insensitive"
        assert len(fts_antibodies(search="FastImmune PE Mouse").items) == 1
        assert len(fts_antibodies(search="BD FastImmune™ PE Mouse Anti-Human IL-8").items) == 1
        assert len(fts_antibodies(search="BD FastImmune™ PE Mouse (Anti-Human) IL-8").items) == 1, "Must ignore special characters"

        assert len(fts_antibodies(search="Sheep polyclonal anti-FSH antibody labeled with acridinium ester").items) == 2, "Search in kit contents"

        # assert len(fts_antibodies(search="defining").items) == 2, "Search in defining citation"
        # assert len(fts_antibodies(search="citation").items) == 1, "Search in defining citation specificity"

        assert len(fts_antibodies(search="External validation DATA SET is released testing").items) == 1, "Search in comments"
        assert len(fts_antibodies(search="vendorname").items) == 2
        assert len(fts_antibodies(search="Andrew Dingwall").items) == 1

        assert len(fts_antibodies(search="rabbit").items) == 1, "Search in source organism"
        assert len(fts_antibodies(search="Rabbit").items) == 1, "case insensitive search"
        assert len(fts_antibodies(search="Andrew Dingwall").items) == 1

    def test_update(self):
        user_id = "aaaa"
        new_name = "My updated abName"
        ab = create_antibody(AddAntibodyDTO(**example_ab), user_id)
        user_antibodies = get_user_antibodies(user_id, 0, 1)
        ab_to_update = user_antibodies.items[0]
        self.assertNotEqual(ab.abName, new_name)
        assert ab.abId == ab_to_update.abId
        ab_update_example = dict(example_ab)
        ab_update_example["abName"] = new_name
        updated_ab = update_antibody(
            user_id, ab_to_update.accession, UpdateAntibody(**ab_update_example)
        )
        self.assertEquals(updated_ab.abName, new_name)
        ab_update_example["vendorName"] = "Vendor Update Test"
        with self.assertRaises(AntibodyDataException):
            update_antibody(
                user_id, ab_to_update.accession, AddAntibody(**ab_update_example)
            )

        dao = Antibody.objects.get(ab_id=ab.abId)
        dao.species.set([])
        dao.save()
        assert dao.species.count() == 0
        assert len(dao.target_species_raw) == 0

        dao.target_species_raw = "mouse"
        dao.species.add(Specie.objects.get(name="human"))
        dao.save()
        assert dao.species.count() == 2
        assert "human" in dao.target_species_raw
        assert "mouse" in dao.target_species_raw

        dao.target_species_raw = "mouse,human,rat,human,mouse"
        dao.save()
        assert dao.species.count() == 3

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
        ab = create_antibody(AddAntibodyDTO(**example_ab), "aaaa")
        self.assertEquals(ab.vendorName, V1_N1)
        self.assertTrue(all(v.status == STATUS.QUEUE for v in VendorDomain.objects.all()))
        self.assertEqual(len(ab.vendorUrl), 0, "Vendor URL should not be shown as it's not curated yet")
        self.curate_test_antibody_data(ab.abId)
        self.curate_vendor_domains_for_antibody(ab.abId)
        ab = get_antibody(ab.abId)[0]  ## returns a list - get the first one

        self.assertIn(
            V1_D1,
            ab.vendorUrl,
        )


        # Number of vendors 1 and vendor domain 1
        self.assertEquals(VendorDomain.objects.count(), 1)
        self.assertEquals(Vendor.objects.count(), 1)

        ### both domain and vendor name are not recognized  ###
        # will create a new vendor since both vendor name and url are different
        modified_example_ab = example_ab.copy()
        modified_example_ab["vendorName"] = V2_N1
        modified_example_ab["url"] = "https://" + V2_D1 + "/test"
        modified_example_ab["catalogNum"] = "N176AB_23/35_SD_WEER"
        ab2 = create_antibody(AddAntibodyDTO(**modified_example_ab), "aaaa")
        
        self.curate_test_antibody_data(ab2.abId)
        self.curate_vendor_domains_for_antibody(ab2.abId)
        ab2 = get_antibody(ab2.abId)[0]

        self.assertEqual(ab2.vendorName, V2_N1)
        self.assertNotEqual(ab2.vendorId, ab.vendorId)
        self.assertEqual(ab2.vendorUrl, [V2_D1])

        # Number of vendors 2, vendor domain 2
        self.assertEquals(VendorDomain.objects.count(), 2)
        self.assertEquals(Vendor.objects.count(), 2)

        # Before the vendor synonym is saved in the operation below, check should be empty
        self.assertEquals(VendorSynonym.objects.count(), 0)

        # Both domain and vendor name are recognized ->
        # domain is prioritized and vendor name is added as synonym
        modified_example_ab = example_ab.copy()
        modified_example_ab["url"] = "https://" + V1_D1 + "/test"
        modified_example_ab["vendorName"] = V2_N1
        modified_example_ab["catalogNum"] = "N176AB_23/35_SD"
        ab3 = create_antibody(AddAntibodyDTO(**modified_example_ab), "aaaa")
        self.curate_test_antibody_data(ab3.abId)
        ab3 = get_antibody(ab3.abId)[0]
        self.assertEquals(ab3.vendorName, V1_N1)
        self.assertEqual(ab3.vendorId, ab.vendorId)
        self.assertEqual(ab3.vendorUrl, [V1_D1])

        # Number of vendors 2, vendor domain 2
        self.assertEquals(VendorDomain.objects.count(), 2)
        self.assertEquals(Vendor.objects.count(), 2)

        # the above should add a new vendor synonym
        self.assertEquals(VendorSynonym.objects.count(), 1)

        ### the domain is not recognized but vendor name is recognized. ###
        modified_example_ab = example_ab.copy()
        modified_example_ab["url"] = "https://" + V2_D2
        modified_example_ab["vendorName"] = V2_N1
        modified_example_ab["catalogNum"] = "N176AB_23/35_SD"
        ab4 = create_antibody(AddAntibodyDTO(**modified_example_ab), "aaaa")
        self.curate_test_antibody_data(ab4.abId)
        self.curate_vendor_domains_for_antibody(ab4.abId)
        ab4 = get_antibody(ab4.abId)[0]

        self.assertEquals(ab4.vendorName, ab2.vendorName)
        self.assertEquals(set(ab4.vendorUrl), set([V2_D1, V2_D2]))
        self.assertEqual(ab4.vendorId, ab2.vendorId)

        # Number of vendors 2, vendor domain 3 - the new url is attached to the vendor recognized
        self.assertEqual(set(ab4.vendorUrl), set([V2_D1, V2_D2]))
        self.assertEquals(VendorDomain.objects.count(), 3)
        self.assertEquals(Vendor.objects.count(), 2)

        ### Both domain and vendor name are not recognized ###
        modified_example_ab = example_ab.copy()
        modified_example_ab["url"] = "https://" + V3_D1
        modified_example_ab["vendorName"] = V3_N1
        modified_example_ab["catalogNum"] = "N176AB_23/35_SD_456"
        ab5 = create_antibody(AddAntibodyDTO(**modified_example_ab), "aaaa")
        self.curate_test_antibody_data(ab5.abId)
        ab5 = get_antibody(ab5.abId)[0]

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
        ab6 = create_antibody(AddAntibodyDTO(**modified_example_ab), "aaaa")
        self.curate_test_antibody_data(ab6.abId)
        ab6 = get_antibody(ab6.abId)[0]

        self.assertEquals(ab6.vendorName, ab.vendorName)
        self.assertEqual(ab6.vendorId, ab.vendorId)
        self.assertEqual(ab6.vendorUrl, ab.vendorUrl)

        # A new vendor synonym is added, since vendor name is not recognized
        self.assertEquals(VendorSynonym.objects.count(), 2)
        self.assertEquals(Vendor.objects.count(), 3)
