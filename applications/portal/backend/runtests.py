#!/usr/bin/env python
import os
import sys

import django
from django.conf import settings
from django.test.utils import get_runner

HERE = os.path.dirname(os.path.realpath(__file__))
os.environ["CH_VALUES_PATH"] = os.path.join(HERE, "api/tests/resources", "values.yaml")
os.environ["DJANGO_SETTINGS_MODULE"] = "portal.settings"
os.environ["CH_CURRENT_APP_NAME"] = "portal"
os.environ["NINJA_SKIP_REGISTRY"] = "1"


def path_to_module(p):
    # If it's already a Python module path (e.g., api.tests.test_antibodies), return it as-is
    if "." in p and "/" not in p and "\\" not in p:
        return p
    
    # Handle absolute paths
    if "/" in p and not p.endswith(".py") and "test_" not in p:
        return None
    if p.endswith(".py"):
        p = p[:-3]
    
    # Convert file paths to module paths
    if "portal/backend/" in p:
        p = p.split("portal/backend/")[1]
    return p.replace("/", ".").replace("\\", ".").replace("-", "_")


if __name__ == "__main__":

    print(os.environ)

    tests = [path_to_module(p) for p in sys.argv[1:]]
    tests = [t for t in tests if t]
    if len(tests) == 0:
        tests = ["api.tests"]

    django.setup()
    TestRunner = get_runner(settings)
    test_runner = TestRunner(exclude_tags=[])
    failures = test_runner.run_tests(tests)
    sys.exit(bool(failures))
