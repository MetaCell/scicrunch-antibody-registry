from .test_vendor_admin import VendorAdminTests
from .test_search_filter import SearchAndFilterAntibodiesTestCase
from .test_antibodies import AntibodiesTestCase
import os
os.environ["TEST"] = "True"
