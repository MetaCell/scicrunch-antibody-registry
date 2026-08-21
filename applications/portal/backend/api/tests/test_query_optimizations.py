"""
Tests for the slow-query optimizations (ANTIBODY-REGISTRY-5F, ANTIBODY-REGISTRY-5M):
- conditional DISTINCT on search/filter querysets (only when an M2M relation is spanned)
- PrecomputedCountPaginator avoiding duplicate COUNT queries
- /api/antibodies serving the total from the AntibodyStats cache
"""
from django.contrib.auth.models import User
from django.db import connection
from django.test import SimpleTestCase, TestCase
from django.test.utils import CaptureQueriesContext

from api.api import api
from api.models import Antibody, AntibodyStats, STATUS
from api.repositories.filtering_utils import filters_require_distinct
from api.repositories.search_repository import PrecomputedCountPaginator
from api.schemas import (
    FilterRequest,
    KeyValueArrayPair,
    KeyValuePair,
    KeyValueSortOrderPair,
    SortOrderEnum,
)
from cloudharness.middleware import set_authentication_token
from cloudharness_django.models import Member

from .data.test_data import example_ab
from .test_plain_filter import token
from .utils import AnonymousTestClient, LoggedinTestClient


class FiltersRequireDistinctTests(SimpleTestCase):
    def test_no_filters(self):
        self.assertFalse(filters_require_distinct(None))
        self.assertFalse(filters_require_distinct(FilterRequest()))

    def test_plain_column_filters_do_not_require_distinct(self):
        filters = FilterRequest(
            contains=[KeyValuePair(key="ab_name", value="sars")],
            equals=[KeyValuePair(key="clonality", value="polyclonal")],
            is_any_of=[KeyValueArrayPair(key="catalog_num", value=["N176A/35"])],
        )
        self.assertFalse(filters_require_distinct(filters))

    def test_foreign_key_filters_do_not_require_distinct(self):
        # forward FK joins (vendor, source_organism) cannot duplicate rows
        filters = FilterRequest(
            contains=[KeyValuePair(key="vendor", value="abcam")],
            equals=[KeyValuePair(key="source_organism", value="mouse")],
        )
        self.assertFalse(filters_require_distinct(filters))

    def test_m2m_filter_keys_require_distinct(self):
        for filters in [
            FilterRequest(contains=[KeyValuePair(key="species", value="mouse")]),
            FilterRequest(equals=[KeyValuePair(key="applications", value="ELISA")]),
            FilterRequest(starts_with=[KeyValuePair(key="species", value="mo")]),
            FilterRequest(ends_with=[KeyValuePair(key="applications", value="SA")]),
            FilterRequest(is_any_of=[KeyValueArrayPair(key="species", value=["mouse", "human"])]),
            FilterRequest(is_empty=["species"]),
            FilterRequest(is_not_empty=["applications"]),
        ]:
            self.assertTrue(filters_require_distinct(filters), filters)

    def test_m2m_sort_keys_require_distinct(self):
        self.assertTrue(filters_require_distinct(FilterRequest(
            sort_on=[KeyValueSortOrderPair(key="species", sortorder=SortOrderEnum.asc)])))
        self.assertFalse(filters_require_distinct(FilterRequest(
            sort_on=[KeyValueSortOrderPair(key="catalog_num", sortorder=SortOrderEnum.desc)])))


class PrecomputedCountPaginatorTests(SimpleTestCase):
    def test_uses_precomputed_count(self):
        p = PrecomputedCountPaginator(list(range(10)), 5, 1000)
        self.assertEqual(p.count, 1000)
        self.assertEqual(p.num_pages, 200)

    def test_page_slicing_unaffected(self):
        p = PrecomputedCountPaginator(list(range(10)), 5, 10)
        self.assertEqual(list(p.get_page(2)), [5, 6, 7, 8, 9])


class GetAntibodiesCachedCountTestCase(TestCase):
    """GET /api/antibodies must serve total_elements from AntibodyStats on the
    unfiltered CURATED path and fall back to a live count everywhere else."""

    def setUp(self):
        self.test_user = User.objects.create_user(
            username='testuser', email='test@example.com', password='testpass123')
        set_authentication_token(token)
        self.client = LoggedinTestClient(api, self.test_user)
        self.anon_client = AnonymousTestClient(api)
        Member.objects.create(kc_id="66a9dd54-2214-4ed7-b4f8-daa5bf3c9a79", user=self.test_user)

        response = self.client.post("/antibodies", json=example_ab)
        self.assertEqual(response.status_code, 201)
        antibody = Antibody.objects.get(ab_id=response.json()['abId'])
        antibody.status = STATUS.CURATED
        antibody.save()

    def set_cached_count(self, count):
        AntibodyStats.objects.update_or_create(
            status=STATUS.CURATED, defaults={"count": count})

    def test_unfiltered_curated_listing_uses_cached_count(self):
        # a sentinel diverging from the live count proves the cache is read
        self.set_cached_count(999)
        response = self.anon_client.get("/antibodies")
        self.assertEqual(response.status_code, 200)
        result = response.json()
        self.assertEqual(result['totalElements'], 999)
        self.assertEqual(len(result['items']), 1)

    def test_unfiltered_curated_listing_issues_no_count_query(self):
        self.set_cached_count(1)
        with CaptureQueriesContext(connection) as ctx:
            response = self.anon_client.get("/antibodies")
        self.assertEqual(response.status_code, 200)
        count_queries = [q['sql'] for q in ctx.captured_queries if 'COUNT(' in q['sql'].upper()]
        self.assertEqual(count_queries, [])

    def test_date_filtered_listing_uses_live_count(self):
        self.set_cached_count(999)
        response = self.anon_client.get("/antibodies?updated_from=2000-01-01")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['totalElements'], 1)

        response = self.anon_client.get("/antibodies?updated_to=2000-01-01")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['totalElements'], 0)

    def test_non_curated_status_uses_live_count(self):
        self.set_cached_count(999)
        response = self.client.post("/antibodies", json={**example_ab, "catalogNum": "QQ123"})
        self.assertEqual(response.status_code, 201)  # stays in QUEUE

        response = self.anon_client.get("/antibodies?status=QUEUE")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['totalElements'], 1)

    def test_missing_stats_row_falls_back_to_live_count(self):
        AntibodyStats.objects.all().delete()
        response = self.anon_client.get("/antibodies")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['totalElements'], 1)


class SearchDistinctTestCase(TestCase):
    """Filtering on M2M relations (species, applications) joins multiple rows
    per antibody; counts and items must be deduplicated in every search path."""

    # example_ab has targetSpecies ["mouse", "human"]: an is_any_of filter
    # matching both species produces two joined rows for one antibody, so a
    # missing DISTINCT would double both totalElements and items
    species_filter = [{"key": "species", "value": ["mouse", "human"]}]

    def setUp(self):
        self.test_user = User.objects.create_user(
            username='testuser', email='test@example.com', password='testpass123')
        set_authentication_token(token)
        self.client = LoggedinTestClient(api, self.test_user)
        Member.objects.create(kc_id="66a9dd54-2214-4ed7-b4f8-daa5bf3c9a79", user=self.test_user)

        response = self.client.post("/antibodies", json=example_ab)
        self.assertEqual(response.status_code, 201)
        self.antibody = Antibody.objects.get(ab_id=response.json()['abId'])
        self.antibody.status = STATUS.CURATED
        self.antibody.save()

        self.filter_request = {
            "search": "",
            "contains": [],
            "equals": [],
            "startsWith": [],
            "endsWith": [],
            "isEmpty": [],
            "isNotEmpty": [],
            "isAnyOf": self.species_filter,
            "size": 10,
            "page": 1,
            "sortOn": [],
            "operation": "and",
            "isUserScope": False,
        }

    def assert_no_duplicates(self, body):
        response = self.client.post("/search/antibodies", json=body)
        self.assertEqual(response.status_code, 200)
        result = response.json()
        self.assertEqual(result['totalElements'], 1)
        self.assertEqual(len(result['items']), 1)
        self.assertEqual(result['items'][0]['catalogNum'], example_ab["catalogNum"])

    def test_filter_only_path_deduplicates(self):
        self.assert_no_duplicates(self.filter_request)

    def test_fts_path_deduplicates(self):
        # "mouse" appears in example_ab's ab_name; no digits in the term, so
        # the catalog-number branch is skipped and the tsquery branch of
        # fts_and_filter_search is exercised
        self.assert_no_duplicates({**self.filter_request, "search": "mouse"})

    def test_user_scoped_plain_filter_deduplicates(self):
        self.assert_no_duplicates({**self.filter_request, "isUserScope": True})

    def test_m2m_sorting_deduplicates(self):
        response = self.client.post("/search/antibodies", json={
            **self.filter_request,
            "isAnyOf": [],
            "sortOn": [{"key": "species", "sortorder": "asc"}],
        })
        self.assertEqual(response.status_code, 200)
        result = response.json()
        self.assertEqual(result['totalElements'], 1)
        self.assertEqual(len(result['items']), 1)
