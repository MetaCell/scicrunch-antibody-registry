import os
os.environ["TEST"] = "True"

from .test_antibodies import AntibodiesTestCase
from .test_search_filter import SearchAndFilterAntibodiesTestCase
from .test_vendor_admin import VendorAdminTests

