from .test_vendor_admin import VendorAdminTests
from .test_search_filter import SearchAndFilterAntibodiesTestCase
from .test_antibodies import AntibodiesTestCase
from .test_ttl_cache import TTLCacheTestCase
import os
os.environ["TEST"] = "True"
