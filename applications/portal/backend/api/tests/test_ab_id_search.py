from django.test import TestCase

from api.models import Antibody, STATUS, Vendor
from api.routers import search
from .utils import AnonymousTestClient


class AbIdSearchTestCase(TestCase):
    """
    GET /fts-antibodies resolves an AB id by exact lookup, and reports the link
    like every other endpoint. It used to hand already-mapped DTOs to the
    response schema, whose url resolver reads model-only attributes, so every
    result came back with url=None regardless of show_link.
    """

    def setUp(self):
        self.client = AnonymousTestClient(search.router)
        self.linking_vendor = Vendor.objects.create(name="Linking Vendor", show_link=True)
        self.hiding_vendor = Vendor.objects.create(name="Hiding Vendor", show_link=False)

    def _make(self, ab_id, show_link, vendor):
        return Antibody.objects.create(
            ab_id=ab_id,
            accession=ab_id,
            ab_name="Fts Link Test",
            url=f"https://example.com/{ab_id}",
            show_link=show_link,
            vendor=vendor,
            status=STATUS.CURATED,
        )

    def _search(self, ab_id):
        response = self.client.get(f"/fts-antibodies?q=AB_{ab_id}")
        self.assertEqual(response.status_code, 200)
        items = response.json()["items"]
        self.assertEqual(len(items), 1)
        return items[0]

    def test_explicit_show_link_returns_url(self):
        ab = self._make("21001", True, self.linking_vendor)
        item = self._search(ab.ab_id)
        self.assertTrue(item["showLink"])
        self.assertEqual(item["url"], "https://example.com/21001")

    def test_show_link_inherited_from_vendor_returns_url(self):
        ab = self._make("21002", None, self.linking_vendor)
        item = self._search(ab.ab_id)
        self.assertTrue(item["showLink"])
        self.assertEqual(item["url"], "https://example.com/21002")

    def test_hidden_link_withholds_url(self):
        ab = self._make("21003", False, self.linking_vendor)
        item = self._search(ab.ab_id)
        self.assertFalse(item["showLink"])
        self.assertIsNone(item["url"])

    def test_hidden_link_inherited_from_vendor_withholds_url(self):
        ab = self._make("21004", None, self.hiding_vendor)
        item = self._search(ab.ab_id)
        self.assertFalse(item["showLink"])
        self.assertIsNone(item["url"])

    def test_other_fields_still_serialized(self):
        """An AB id lookup keeps returning the rest of the record"""
        ab = self._make("21005", True, self.linking_vendor)
        item = self._search(ab.ab_id)
        self.assertEqual(item["abId"], 21005)
        self.assertEqual(item["vendorName"], "Linking Vendor")

    def test_malformed_ab_id_returns_empty(self):
        response = self.client.get("/fts-antibodies?q=AB_notanumber")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["items"], [])

    def test_unknown_ab_id_returns_empty(self):
        response = self.client.get("/fts-antibodies?q=AB_99999999")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["items"], [])

    def test_rrid_prefix_resolves_to_the_record(self):
        """A whole RRID pasted into search resolves like the bare AB id"""
        ab = self._make("21006", True, self.linking_vendor)
        response = self.client.get(f"/fts-antibodies?q=RRID:AB_{ab.ab_id}")
        self.assertEqual(response.status_code, 200)
        items = response.json()["items"]
        self.assertEqual(len(items), 1)
        self.assertEqual(items[0]["abId"], 21006)
        self.assertEqual(items[0]["url"], "https://example.com/21006")


class FilterSearchAbIdTestCase(TestCase):
    """
    POST /search/antibodies resolves an AB id by exact lookup too. It used to
    hand the prefixed id to full text search, which tokenizes to the bare
    number and matched nothing.
    """

    def setUp(self):
        self.client = AnonymousTestClient(search.router)
        self.vendor = Vendor.objects.create(name="Filter Vendor", show_link=True)
        self.antibody = Antibody.objects.create(
            ab_id="22001",
            accession="22001",
            ab_name="Filter Search Test",
            url="https://example.com/22001",
            show_link=True,
            vendor=self.vendor,
            status=STATUS.CURATED,
        )

    def _post(self, body):
        response = self.client.post(
            "/search/antibodies", json=body, content_type="application/json")
        self.assertEqual(response.status_code, 200)
        return response.json()

    def test_ab_id_search_finds_the_record(self):
        data = self._post({"search": "AB_22001", "page": 1, "size": 10})
        self.assertEqual(data["totalElements"], 1)
        self.assertEqual(data["items"][0]["abId"], 22001)
        self.assertEqual(data["items"][0]["url"], "https://example.com/22001")

    def test_rrid_search_finds_the_record(self):
        data = self._post({"search": "RRID:AB_22001", "page": 1, "size": 10})
        self.assertEqual(data["totalElements"], 1)
        self.assertEqual(data["items"][0]["abId"], 22001)

    def test_second_page_of_a_single_match_is_empty(self):
        data = self._post({"search": "AB_22001", "page": 2, "size": 10})
        self.assertEqual(data["items"], [])

    def test_absent_search_term_does_not_error(self):
        """A filter-only request carries no search term and used to 500"""
        data = self._post({"page": 1, "size": 10})
        self.assertGreaterEqual(data["totalElements"], 1)
