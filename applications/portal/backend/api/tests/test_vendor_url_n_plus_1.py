from django.db import connection
from django.test import TestCase
from django.test.utils import CaptureQueriesContext

from api.models import Antibody, STATUS, Vendor, VendorDomain


class VendorUrlNPlus1TestCase(TestCase):
    """
    Regression test for ANTIBODY-REGISTRY-5D: serializing a list of antibodies
    should not issue one VendorDomain query per antibody.
    """

    def setUp(self):
        self.vendors = []
        for i in range(5):
            vendor = Vendor.objects.create(name=f"Vendor {i}")
            VendorDomain.objects.create(
                vendor=vendor, base_url=f"vendor{i}.example.com", status=STATUS.CURATED
            )
            self.vendors.append(vendor)
            Antibody.objects.create(
                ab_id=1000 + i, accession=1000 + i, ab_name="", catalog_num=f"CAT-{i}",
                status=STATUS.CURATED, vendor=vendor,
            )

    def test_without_prefetch_is_n_plus_1(self):
        """Sanity check: confirms the bug exists without the fix (would fail if
        VendorDomain lookups ever stopped happening per-antibody some other way)."""
        antibodies = list(Antibody.objects.filter(status=STATUS.CURATED).select_related("vendor"))
        with CaptureQueriesContext(connection) as ctx:
            for a in antibodies:
                list(VendorDomain.objects.filter(vendor_id=a.vendor_id, status=STATUS.CURATED))
        self.assertEqual(len(ctx.captured_queries), len(antibodies))

    def test_with_curated_vendor_domains_is_one_query(self):
        with CaptureQueriesContext(connection) as ctx:
            antibodies = list(
                Antibody.objects.filter(status=STATUS.CURATED)
                .select_related("vendor")
                .with_curated_vendor_domains()
            )
            # Force resolver-equivalent access, same as AntibodySchema.resolve_vendor_url
            urls_by_antibody = {
                a.ix: [vd.base_url for vd in getattr(a.vendor, "curated_domains", [])]
                for a in antibodies
            }

        vendor_domain_queries = [
            q for q in ctx.captured_queries if "api_vendordomain" in q["sql"]
        ]
        self.assertEqual(
            len(vendor_domain_queries), 1,
            f"Expected exactly 1 VendorDomain query, got {len(vendor_domain_queries)}: "
            f"{[q['sql'] for q in vendor_domain_queries]}"
        )
        self.assertEqual(len(urls_by_antibody), 5)
        for i, vendor in enumerate(self.vendors):
            antibody = Antibody.objects.get(ab_id=1000 + i)
            self.assertEqual(urls_by_antibody[antibody.ix], [f"vendor{i}.example.com"])
