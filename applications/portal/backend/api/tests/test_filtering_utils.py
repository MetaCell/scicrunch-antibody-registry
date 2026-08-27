"""
Unit tests for api.repositories.filtering_utils.

These cover field-name validation only and never hit the database: unknown
field names must be rejected as a 400 before they reach the ORM, where they
would raise a FieldError and surface as a 500 (ANTIBODY-REGISTRY-53, -7S, -5E).
"""
from django.test import SimpleTestCase
from ninja.errors import HttpError

from api.repositories.filtering_utils import (
    check_filters_are_valid,
    order_by_string,
)
from api.schemas import (
    FilterRequest,
    KeyValuePair,
    KeyValueSortOrderPair,
    SortOrderEnum,
)


def sort_request(key, sortorder=SortOrderEnum.asc):
    return FilterRequest(sort_on=[KeyValueSortOrderPair(key=key, sortorder=sortorder)])


class FilteringUtilsTestCase(SimpleTestCase):

    # order_by_string

    def test_no_filters_or_no_sort_on_returns_empty(self):
        self.assertEqual(order_by_string(None), [])
        self.assertEqual(order_by_string(FilterRequest()), [])

    def test_valid_key_ascending(self):
        self.assertEqual(order_by_string(sort_request("ab_name")), ["ab_name"])

    def test_valid_key_descending_is_prefixed(self):
        self.assertEqual(
            order_by_string(sort_request("ab_name", SortOrderEnum.desc)), ["-ab_name"]
        )

    def test_foreign_key_field_is_not_traversed_to_name(self):
        # Vendor/Specie/Application declare Meta.ordering = ('name',), so Django
        # already orders by the related name. Forcing "vendor__name" here changes
        # the join shape and produces a different (wrong) order once combined with
        # the .distinct() in search_repository.fts_and_filter_search.
        self.assertEqual(order_by_string(sort_request("vendor")), ["vendor"])
        self.assertEqual(order_by_string(sort_request("applications")), ["applications"])

    def test_multiple_sort_keys_keep_request_order(self):
        filters = FilterRequest(
            sort_on=[
                KeyValueSortOrderPair(key="vendor", sortorder=SortOrderEnum.asc),
                KeyValueSortOrderPair(key="catalog_num", sortorder=SortOrderEnum.desc),
            ]
        )
        self.assertEqual(order_by_string(filters), ["vendor", "-catalog_num"])

    def test_camel_case_sort_keys_are_rejected(self):
        # The exact keys seen in Sentry: API clients mirroring the camelCase field
        # names from the *response* schema. These are not sortable field names and
        # must not be silently reinterpreted.
        for key in ("numOfCitation", "definingCitation", "abTarget", "abName"):
            with self.subTest(key=key):
                with self.assertRaises(HttpError) as ctx:
                    order_by_string(sort_request(key))
                self.assertEqual(ctx.exception.status_code, 400)

    def test_unknown_sort_key_is_rejected(self):
        with self.assertRaises(HttpError) as ctx:
            order_by_string(sort_request("does_not_exist"))
        self.assertEqual(ctx.exception.status_code, 400)

    def test_non_sortable_model_field_is_rejected(self):
        # A real Antibody field, but deliberately not in FILTERABLE_AND_SORTABLE_FIELDS
        with self.assertRaises(HttpError) as ctx:
            order_by_string(sort_request("defining_citation"))
        self.assertEqual(ctx.exception.status_code, 400)

    # check_filters_are_valid

    def test_rejects_non_filter_request(self):
        self.assertFalse(check_filters_are_valid({"contains": []}))

    def test_empty_request_is_valid(self):
        self.assertTrue(check_filters_are_valid(FilterRequest()))

    def test_valid_keys_across_filter_types(self):
        filters = FilterRequest(
            contains=[KeyValuePair(key="ab_name", value="x")],
            equals=[KeyValuePair(key="catalog_num", value="y")],
            starts_with=[KeyValuePair(key="clone_id", value="z")],
            ends_with=[KeyValuePair(key="comments", value="w")],
            is_empty=["accession"],
            is_not_empty=["citation"],
            sort_on=[KeyValueSortOrderPair(key="vendor", sortorder=SortOrderEnum.asc)],
        )
        self.assertTrue(check_filters_are_valid(filters))

    def test_unknown_key_in_any_filter_type_is_invalid(self):
        cases = {
            "contains": FilterRequest(contains=[KeyValuePair(key="abName", value="x")]),
            "equals": FilterRequest(equals=[KeyValuePair(key="abName", value="x")]),
            "starts_with": FilterRequest(starts_with=[KeyValuePair(key="abName", value="x")]),
            "ends_with": FilterRequest(ends_with=[KeyValuePair(key="abName", value="x")]),
            "is_empty": FilterRequest(is_empty=["definingCitation"]),
            "is_not_empty": FilterRequest(is_not_empty=["definingCitation"]),
            "sort_on": sort_request("numOfCitation"),
        }
        for filter_type, filters in cases.items():
            with self.subTest(filter_type=filter_type):
                self.assertFalse(check_filters_are_valid(filters))
