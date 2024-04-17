from django.test import TestCase
from django.contrib.admin.sites import AdminSite
from api.services.antibody_service import *
from api.models import Vendor, VendorDomain

from ..admin import VendorAdmin
from ..models import Vendor, Antibody, VendorDomain


class VendorAdminTests(TestCase):

    def setUp(self):
        self.site = AdminSite()

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
