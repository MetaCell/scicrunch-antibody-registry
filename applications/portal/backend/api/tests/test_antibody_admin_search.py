"""
Tests for the routed admin changelist search (AntibodyAdmin.get_search_results).

The search tries the identifying fields by exact match, in a fixed order, and
only falls back to full text when none of them hits. These tests pin both
halves: which field wins for a given term, and that the fallback still finds
records by words that live nowhere in the exact-match fields.
"""
from django.contrib.admin.sites import AdminSite
from django.contrib.auth.models import User
from django.test import RequestFactory, TestCase, override_settings

from ..admin import AntibodyAdmin, ResultLimitFilter
from ..models import STATUS, Antibody, Vendor


class AntibodyAdminSearchTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.abcam = Vendor.objects.create(name="Abcam")
        cls.other_vendor = Vendor.objects.create(name="Novus")
        cls.curator = User.objects.create_user(
            "curator", "curator@example.com", "pw")

        cls.tubulin = Antibody.objects.create(
            vendor=cls.abcam, owner=cls.curator, ab_id="384011", accession="384011",
            catalog_num="GTX76403", ab_name="anti-Tubulin beta-3 monoclonal",
            clone_id="IF4", status=STATUS.CURATED, url="https://example.com")
        cls.atrip = Antibody.objects.create(
            vendor=cls.other_vendor, ab_id="942163", accession="942163",
            catalog_num="ab56956", ab_name="ATRIP antibody",
            status=STATUS.CURATED, url="https://example.com")

    def setUp(self):
        self.admin = AntibodyAdmin(Antibody, AdminSite())
        request = RequestFactory().get("/admin/api/antibody/")
        request.user = User.objects.create_superuser("admin", "a@example.com", "pw")
        self.request = request

    def search(self, term):
        queryset, may_have_duplicates = self.admin.get_search_results(
            self.request, Antibody.objects.all(), term)
        self.assertFalse(may_have_duplicates)
        return set(queryset.values_list("ix", flat=True))

    # -- exact-match routes -------------------------------------------------

    def test_matches_ab_id(self):
        self.assertEqual(self.search("384011"), {self.tubulin.ix})

    def test_matches_ab_id_with_ab_prefix(self):
        # the changelist's own ab_id column renders as "AB_384011"
        self.assertEqual(self.search("AB_384011"), {self.tubulin.ix})

    def test_matches_ab_id_with_rrid_prefix(self):
        self.assertEqual(self.search("RRID:AB_384011"), {self.tubulin.ix})
        self.assertEqual(self.search("rrid:ab_384011"), {self.tubulin.ix})

    def test_matches_catalog_num_case_insensitively(self):
        self.assertEqual(self.search("GTX76403"), {self.tubulin.ix})
        self.assertEqual(self.search("gtx76403"), {self.tubulin.ix})

    def test_matches_submitter_email(self):
        self.assertEqual(self.search("curator@example.com"), {self.tubulin.ix})
        self.assertEqual(self.search("CURATOR@example.com"), {self.tubulin.ix})

    def test_matches_vendor_name(self):
        self.assertEqual(self.search("Abcam"), {self.tubulin.ix})
        self.assertEqual(self.search("abcam"), {self.tubulin.ix})

    def test_exact_match_is_not_a_substring_match(self):
        # a partial catalog number is not an exact hit, so it routes to full
        # text -- which does not index catalog numbers, hence no results
        self.assertEqual(self.search("76403"), set())

    # -- full-text fallback -------------------------------------------------

    def test_falls_back_to_full_text_on_ab_name(self):
        # "Tubulin" is in no exact-match field; only the search vector has it
        self.assertEqual(self.search("Tubulin"), {self.tubulin.ix})

    def test_falls_back_to_full_text_on_clone_id(self):
        self.assertEqual(self.search("IF4"), {self.tubulin.ix})

    def test_full_text_ands_multiple_words(self):
        self.assertEqual(self.search("Tubulin monoclonal"), {self.tubulin.ix})
        self.assertEqual(self.search("Tubulin ATRIP"), set())

    def test_no_match_returns_nothing(self):
        self.assertEqual(self.search("nosuchantibody"), set())

    def test_blank_term_returns_everything(self):
        self.assertEqual(self.search("   "), {self.tubulin.ix, self.atrip.ix})

    # -- route priority -----------------------------------------------------

    def test_exact_match_wins_over_full_text(self):
        # "ATRIP" is both this record's exact-ish name and a full-text token;
        # the catalog number of the *other* record must not leak in
        self.assertEqual(self.search("ab56956"), {self.atrip.ix})

    def test_full_result_count_is_not_computed(self):
        # the extra COUNT(*) over every row that django adds for the
        # "(N total)" figure is off; it cost a full scan of the table
        self.assertFalse(self.admin.show_full_result_count)


class AdminResultLimitTests(TestCase):
    """
    The changelist search returns at most AntibodyAdmin.result_limit() rows,
    chosen in the sidebar and defaulting to the configured
    settings.ADMIN_SEARCH_RESULT_LIMIT.
    """

    @classmethod
    def setUpTestData(cls):
        vendor = Vendor.objects.create(name="Bulk vendor")
        for n in range(7):
            Antibody.objects.create(
                vendor=vendor, ab_id=f"77{n}", accession=f"77{n}",
                catalog_num=f"BULK{n}", ab_name="repeated widget antibody",
                status=STATUS.CURATED, url="https://example.com")

    def setUp(self):
        self.admin = AntibodyAdmin(Antibody, AdminSite())
        self.user = User.objects.create_superuser("admin", "a@example.com", "pw")

    def request(self, **params):
        request = RequestFactory().get("/admin/api/antibody/", params)
        request.user = self.user
        return request

    def search(self, term="repeated", **params):
        queryset, _ = self.admin.get_search_results(
            self.request(**params), Antibody.objects.all(), term)
        return queryset

    @override_settings(ADMIN_SEARCH_RESULT_LIMIT_ENABLED=True,
                       ADMIN_SEARCH_RESULT_LIMIT=3)
    def test_search_is_bounded_by_the_configured_default(self):
        self.assertEqual(self.search().count(), 3)

    @override_settings(ADMIN_SEARCH_RESULT_LIMIT_ENABLED=True,
                       ADMIN_SEARCH_RESULT_LIMIT=3,
                       ADMIN_SEARCH_RESULT_LIMIT_CHOICES=[3, 5])
    def test_sidebar_choice_overrides_the_default(self):
        self.assertEqual(self.search(result_limit="5").count(), 5)

    @override_settings(ADMIN_SEARCH_RESULT_LIMIT_ENABLED=True,
                       ADMIN_SEARCH_RESULT_LIMIT=3,
                       ADMIN_SEARCH_RESULT_LIMIT_CHOICES=[3, 5])
    def test_no_limit_choice_returns_everything(self):
        self.assertEqual(self.search(result_limit="all").count(), 7)

    @override_settings(ADMIN_SEARCH_RESULT_LIMIT_ENABLED=True,
                       ADMIN_SEARCH_RESULT_LIMIT=3,
                       ADMIN_SEARCH_RESULT_LIMIT_CHOICES=[3, 5])
    def test_unoffered_limit_falls_back_to_the_default(self):
        # an arbitrary limit through the query string is an arbitrarily
        # expensive query, so it is ignored rather than honoured
        self.assertEqual(self.search(result_limit="999").count(), 3)
        self.assertEqual(self.search(result_limit="nonsense").count(), 3)

    @override_settings(ADMIN_SEARCH_RESULT_LIMIT_ENABLED=False,
                       ADMIN_SEARCH_RESULT_LIMIT=3)
    def test_disabling_the_limit_returns_everything(self):
        self.assertEqual(self.search().count(), 7)
        self.assertIsNone(self.admin.result_limit(self.request()))

    @override_settings(ADMIN_SEARCH_RESULT_LIMIT_ENABLED=True,
                       ADMIN_SEARCH_RESULT_LIMIT=3)
    def test_limit_also_bounds_an_exact_match_route(self):
        # a vendor with many antibodies is an exact match, not a fallback
        self.assertEqual(self.search(term="Bulk vendor").count(), 3)

    @override_settings(ADMIN_SEARCH_RESULT_LIMIT_ENABLED=True,
                       ADMIN_SEARCH_RESULT_LIMIT=3)
    def test_browsing_without_a_search_is_not_bounded(self):
        # the limit is on searching; an unfiltered changelist still counts
        # everything, so "select all N" there stays truthful
        queryset, _ = self.admin.get_search_results(
            self.request(), Antibody.objects.all(), "")
        self.assertEqual(queryset.count(), 7)

    @override_settings(ADMIN_SEARCH_RESULT_LIMIT_ENABLED=True,
                       ADMIN_SEARCH_RESULT_LIMIT=3,
                       ADMIN_SEARCH_RESULT_LIMIT_CHOICES=[3, 5])
    def test_sidebar_offers_the_choices_and_marks_the_default(self):
        changelist = self.admin.get_changelist_instance(self.request())
        limit_filter = next(f for f in changelist.get_filters(self.request())[0]
                            if isinstance(f, ResultLimitFilter))
        rendered = list(limit_filter.choices(changelist))
        self.assertEqual([c["display"] for c in rendered],
                         ["3", "5", "No limit (slow)"])
        self.assertEqual([c["display"] for c in rendered if c["selected"]], ["3"])

    @override_settings(ADMIN_SEARCH_RESULT_LIMIT_ENABLED=True,
                       ADMIN_SEARCH_RESULT_LIMIT=3,
                       ADMIN_SEARCH_RESULT_LIMIT_CHOICES=[3, 5])
    def test_sidebar_marks_the_selected_choice(self):
        request = self.request(result_limit="5")
        changelist = self.admin.get_changelist_instance(request)
        limit_filter = next(f for f in changelist.get_filters(request)[0]
                            if isinstance(f, ResultLimitFilter))
        self.assertEqual(
            [c["display"] for c in limit_filter.choices(changelist) if c["selected"]],
            ["5"])
