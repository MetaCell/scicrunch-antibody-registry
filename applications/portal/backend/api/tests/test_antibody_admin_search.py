"""
Tests for the admin changelist search on antibodies (migration 0024).

The trigram indexes added in that migration exist to make the search fast
*without* changing what it matches, so these tests pin the substring semantics:
if search_fields is ever narrowed to "^"/"=" prefixes to chase speed, the
matches that admins rely on disappear and these fail.
"""
from django.contrib.admin.sites import AdminSite
from django.test import RequestFactory, TestCase
from django.contrib.auth.models import User

from ..admin import AntibodyAdmin
from ..models import Antibody, Vendor


class AntibodyAdminSearchTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        vendor = Vendor.objects.create(name="Test vendor")
        cls.tubulin = Antibody.objects.create(
            vendor=vendor, ab_id="384011", catalog_num="GTX76403",
            ab_name="anti-Tubulin beta-3 monoclonal", url="https://example.com")
        cls.atrip = Antibody.objects.create(
            vendor=vendor, ab_id="942163", catalog_num="ab56956",
            ab_name="ATRIP antibody", url="https://example.com")

    def setUp(self):
        self.admin = AntibodyAdmin(Antibody, AdminSite())
        request = RequestFactory().get("/admin/api/antibody/")
        request.user = User.objects.create_superuser("admin", "a@example.com", "pw")
        self.request = request

    def search(self, term):
        queryset, _ = self.admin.get_search_results(
            self.request, Antibody.objects.all(), term)
        return set(queryset.values_list("ix", flat=True))

    def test_matches_ab_name_substring(self):
        # not a prefix of the name: an anchored search would miss it
        self.assertEqual(self.search("Tubulin"), {self.tubulin.ix})

    def test_matches_catalog_num_substring(self):
        self.assertEqual(self.search("76403"), {self.tubulin.ix})

    def test_matches_ab_id_substring(self):
        self.assertEqual(self.search("4216"), {self.atrip.ix})

    def test_search_is_case_insensitive(self):
        self.assertEqual(self.search("atrip"), {self.atrip.ix})
        self.assertEqual(self.search("GTX76403"), {self.tubulin.ix})

    def test_terms_are_anded_across_fields(self):
        # django admin ANDs the words, ORing each one over the search fields
        self.assertEqual(self.search("Tubulin GTX"), {self.tubulin.ix})
        self.assertEqual(self.search("Tubulin ab56956"), set())

    def test_no_match_returns_nothing(self):
        self.assertEqual(self.search("nosuchantibody"), set())

    def test_full_result_count_is_not_computed(self):
        # the extra COUNT(*) over every row that django adds for the
        # "(N total)" figure is off; it cost a full scan of the table
        self.assertFalse(self.admin.show_full_result_count)
