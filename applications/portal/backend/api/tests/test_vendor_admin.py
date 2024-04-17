from django.test import TestCase
from django.contrib.admin.sites import AdminSite
from api.services.antibody_service import *
from api.models import Vendor, VendorDomain, VendorSynonym

from ..admin import VendorAdmin
from ..models import Vendor, Antibody, VendorDomain
from .data.test_data import example_ab
from cloudharness.middleware import set_authentication_token


TOKEN = "eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICJJUHJQcnZBanBrZ19HQlVUSVN5YVBoaXRMeUtVNDlQUGJRUTlPaWNBWEtzIn0.eyJleHAiOjE3MTAyMzg2MDAsImlhdCI6MTcxMDIyNzgwMCwiYXV0aF90aW1lIjoxNzEwMjI3ODAwLCJqdGkiOiIxZTFkMjRmMy0zMTU3LTRhNzEtOGI4Ny0yNzZhZjBkMGFjMTUiLCJpc3MiOiJodHRwczovL2FjY291bnRzLmFyZWcuZGV2Lm1ldGFjZWxsLnVzL2F1dGgvcmVhbG1zL2FyZWciLCJhdWQiOlsid2ViLWNsaWVudCIsImFjY291bnQiXSwic3ViIjoiNjZhOWRkNTQtMjIxNC00ZWQ3LWI0ZjgtZGFhNWJmM2M5YTc5IiwidHlwIjoiQmVhcmVyIiwiYXpwIjoid2ViLWNsaWVudCIsInNlc3Npb25fc3RhdGUiOiI1MzMyNDQ5MS0zNmY4LTRlODctOGE5YS0yZTIyODc3YmQxMDciLCJhY3IiOiIxIiwiYWxsb3dlZC1vcmlnaW5zIjpbIioiXSwicmVhbG1fYWNjZXNzIjp7InJvbGVzIjpbImFkbWluaXN0cmF0b3IiLCJkZWZhdWx0LXJvbGVzLWFyZWciXX0sInJlc291cmNlX2FjY2VzcyI6eyJhY2NvdW50Ijp7InJvbGVzIjpbIm1hbmFnZS1hY2NvdW50IiwibWFuYWdlLWFjY291bnQtbGlua3MiLCJ2aWV3LXByb2ZpbGUiXX19LCJzY29wZSI6Im9wZW5pZCBwcm9maWxlIGFkbWluaXN0cmF0b3Itc2NvcGUgZW1haWwiLCJzaWQiOiI1MzMyNDQ5MS0zNmY4LTRlODctOGE5YS0yZTIyODc3YmQxMDciLCJlbWFpbF92ZXJpZmllZCI6ZmFsc2UsIm5hbWUiOiJGaWxpcHBvIExlZGRhIiwicHJlZmVycmVkX3VzZXJuYW1lIjoiYSIsImdpdmVuX25hbWUiOiJGaWxpcHBvIiwiZmFtaWx5X25hbWUiOiJMZWRkYSIsImVtYWlsIjoiYUBhYS5pdCJ9.RShiiCZPEwz2IxEQqU2TBB1F6NQIOMfcrVU99eMSlXEahb38VegqUyIqUfoQUrQAHqnyysR67HeBuCq2SNh9ctxpAiEpFq7LAkqpEIQfByvdyDsBArT0jeWd6DuQ91_7PAdSPWqFEr-uFo9476NQZecrIuXCaNC3rrHbPb6GZKwT6gUMu_sCYAawT8jA_V9rpfgedM5PuqJHTp40of-ZDchD7Cc2NTIE2RopgkKifxtRRjQ9wwudz0hxKjVb9E9GCtkaA-MjDdEeVxnSgTu2p8Y9EaPOoZKt-zt0XTjRT8otwx7yOzz1euhDVh1-1zBb7V3Lt-w4BW19draYkGWMzg"


class VendorAdminTests(TestCase):

    def setUp(self):
        self.site = AdminSite()
        if TOKEN:
            set_authentication_token(TOKEN)

    def test_force_delete_vendor(self):

        # Create data
        vendor = Vendor.objects.create()

        ab1 = Antibody.objects.create(vendor=vendor, url="https://example.com")

        ab2 = Antibody.objects.create(vendor=vendor, url="https://example.com")

        self.assertEquals(len(Vendor.objects.all()), 1)
        self.assertEquals(len(VendorDomain.objects.all()), 1)

        domain = VendorDomain.objects.create(vendor=vendor)

        self.assertEquals(ab1.vendor, vendor)
        self.assertEquals(ab2.vendor, vendor)
        self.assertEquals(domain.vendor, vendor)
        self.assertEquals(len(Antibody.objects.all()), 2)
        self.assertEquals(len(Vendor.objects.all()), 1)
        self.assertEquals(len(VendorDomain.objects.all()), 2)

        # # Instanciante and tests
        va = VendorAdmin(Vendor, self.site)
        va._force_delete(vendor)
        self.assertEquals(len(Antibody.objects.all()), 0)
        self.assertEquals(len(VendorDomain.objects.all()), 0)
        self.assertEquals(len(Vendor.objects.all()), 1)

    def test_swap_ownership_antibodies(self):
        # Create data
        v1 = Vendor.objects.create(name="v1")
        v2 = Vendor.objects.create(name="v2")
        ab1 = Antibody.objects.create(vendor=v1, url="https://example.com")

        ab2 = Antibody.objects.create(vendor=v1, url="https://example.com")

        domain = VendorDomain.objects.create(vendor=v1)

        self.assertEquals(ab1.vendor, v1)
        self.assertIn(ab1, v1.antibody_set.all())
        self.assertEquals(ab2.vendor, v1)
        self.assertIn(ab2, v1.antibody_set.all())
        self.assertEquals(domain.vendor, v1)
        self.assertEquals(len(Antibody.objects.all()), 2)
        self.assertEquals(len(Vendor.objects.all()), 2)
        self.assertEquals(len(VendorDomain.objects.all()), 2)

        # Instanciante and tests
        va = VendorAdmin(Vendor, AdminSite())
        va._swap_ownership(v1, v2)

        self.assertIn(ab1, v2.antibody_set.all())
        self.assertIn(ab2, v2.antibody_set.all())
        self.assertNotIn(ab1, v1.antibody_set.all())
        self.assertNotIn(ab2, v1.antibody_set.all())
        self.assertIn(domain, v2.vendordomain_set.all())
        self.assertNotIn(domain, v1.vendordomain_set.all())
        self.assertEquals(len(Antibody.objects.all()), 2)
        self.assertEquals(len(Vendor.objects.all()), 2)
        # FIXME self.assertEquals(len(VendorDomain.objects.all()), 1)

    @staticmethod
    def curate_test_antibody_data(ab):
        a: Antibody = Antibody.objects.get(ab_id=ab.abId)
        a.status = STATUS.CURATED
        a.save()

    @staticmethod
    def curate_all_vendor_domains(ab):
        a: Antibody = Antibody.objects.get(ab_id=ab.abId)
        for domain in a.vendor.vendordomain_set.all():
            domain.status = STATUS.CURATED
            domain.save()

    def test_create_vendor_from_antibody(self):
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

        ### first antibody ###
        ab = create_antibody(AddAntibodyDTO(**example_ab), "aaaa")
        self.assertEquals(ab.vendorName, "My vendorname")
        self.assertIn(
            "www.bdbiosciences.com",
            ab.vendorUrl,
        )
        self.curate_test_antibody_data(ab)
        ab = get_antibody(ab.abId)[0]  ## returns a list - get the first one

        self.curate_all_vendor_domains(ab)

        # Number of vendors 1 and vendor domain 1
        self.assertEquals(len(VendorDomain.objects.all()), 1)
        self.assertEquals(len(Vendor.objects.all()), 1)

        ### both domain and vendor name are not recognized  ###
        # will create a new vendor since both vendor name and url are different
        modified_example_ab = example_ab.copy()
        modified_example_ab["vendorName"] = "My vendorname23"
        modified_example_ab["url"] = "https://www.areg.dev.metacell.us"
        modified_example_ab["catalogNum"] = "N176AB_23/35_SD_WEER"
        ab2 = create_antibody(AddAntibodyDTO(**modified_example_ab), "aaaa")
        self.curate_test_antibody_data(ab2)
        self.curate_all_vendor_domains(ab2)
        ab2 = get_antibody(ab2.abId)[0]

        self.assertNotEquals(ab2.vendorName, ab.vendorName)
        self.assertNotEqual(ab2.vendorId, ab.vendorId)
        self.assertNotEqual(ab2.vendorUrl, ab.vendorUrl)

        # Number of vendors 2, vendor domain 2
        self.assertEquals(len(VendorDomain.objects.all()), 2)
        self.assertEquals(len(Vendor.objects.all()), 2)

        # Before the vendor synonym is saved in the operation below, check should be empty
        self.assertEquals(VendorSynonym.objects.count(), 0)

        # Both domain and vendor name are recognized ->
        # domain is prioritized and vendor name is added as synonym
        modified_example_ab = example_ab.copy()
        modified_example_ab["url"] = "https://www.bdbiosciences.com/"
        modified_example_ab["vendorName"] = "My vendorname23"
        modified_example_ab["catalogNum"] = "N176AB_23/35_SD"
        ab3 = create_antibody(AddAntibodyDTO(**modified_example_ab), "aaaa")
        self.curate_test_antibody_data(ab3)
        ab3 = get_antibody(ab3.abId)[0]
        self.assertEquals(ab3.vendorName, ab.vendorName)
        self.assertEqual(ab3.vendorId, ab.vendorId)
        self.assertEqual(ab3.vendorUrl, ab.vendorUrl)

        # Number of vendors 2, vendor domain 2
        self.assertEquals(len(VendorDomain.objects.all()), 2)
        self.assertEquals(len(Vendor.objects.all()), 2)

        # the above should add a new vendor synonym
        self.assertEquals(VendorSynonym.objects.count(), 1)

        ### the domain is not recognized but vendor name is recognized. ###
        modified_example_ab = example_ab.copy()
        modified_example_ab["url"] = "https://www.googol.com/"
        modified_example_ab["vendorName"] = "My vendorname23"
        modified_example_ab["catalogNum"] = "N176AB_23/35_SD"
        ab4 = create_antibody(AddAntibodyDTO(**modified_example_ab), "aaaa")
        self.curate_test_antibody_data(ab4)
        self.curate_all_vendor_domains(ab4)
        ab4 = get_antibody(ab4.abId)[0]

        self.assertEquals(ab4.vendorName, ab2.vendorName)
        self.assertEqual(ab4.vendorId, ab2.vendorId)

        # Number of vendors 2, vendor domain 3 - the new url is attached to the vendor recognized
        self.assertEqual(ab4.vendorUrl, ab2.vendorUrl + ["www.googol.com"])
        self.assertEquals(len(VendorDomain.objects.all()), 3)
        self.assertEquals(len(Vendor.objects.all()), 2)

        ### Both domain and vendor name are not recognized ###
        modified_example_ab = example_ab.copy()
        modified_example_ab["url"] = "https://www.anitbody.com/"
        modified_example_ab["vendorName"] = "John Doe vendorname"
        modified_example_ab["catalogNum"] = "N176AB_23/35_SD_456"
        ab5 = create_antibody(AddAntibodyDTO(**modified_example_ab), "aaaa")
        self.curate_test_antibody_data(ab5)
        ab5 = get_antibody(ab5.abId)[0]

        # this creates a new vendor domain and vendor
        # Number of vendors 3, vendor domain 4
        self.assertEqual(len(VendorDomain.objects.all()), 4)
        self.assertEqual(len(Vendor.objects.all()), 3)

        ### domain is recognized but vendor name is not recognized ###
        # should also create a new vendor synonym
        modified_example_ab = example_ab.copy()
        modified_example_ab["url"] = "https://www.bdbiosciences.com/"
        modified_example_ab["vendorName"] = "Stephen Hawking"
        modified_example_ab["catalogNum"] = "N176AB_23/35_IPL"
        ab6 = create_antibody(AddAntibodyDTO(**modified_example_ab), "aaaa")
        self.curate_test_antibody_data(ab6)
        ab6 = get_antibody(ab6.abId)[0]

        self.assertEquals(ab6.vendorName, ab.vendorName)
        self.assertEqual(ab6.vendorId, ab.vendorId)
        self.assertEqual(ab6.vendorUrl, ab.vendorUrl)

        # A new vendor synonym is added, since vendor name is not recognized
        self.assertEquals(VendorSynonym.objects.count(), 2)
