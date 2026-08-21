# coding: utf-8

import sys

from setuptools import find_packages, setup

NAME = "portal"
VERSION = "1.0.0"

# ---------------------------------------------------------------------------
# REQUIRES is the single source of truth for the backend's Python dependencies.
# requirements.txt is COMPILED from it and must never be edited by hand.
#
# After changing this list, regenerate the lockfile from this directory:
#
#     uv pip compile setup.py -o requirements.txt \
#         --generate-hashes --universal --python-version 3.12
#
# then reinstall and run the tests. See ../README.md#backend-dependencies.
# ---------------------------------------------------------------------------
REQUIRES = [
    # Pinned exactly: the portal is a deployed application rather than a
    # redistributable library, so there is no reason to run against anything
    # other than the versions it was tested with.
    #
    # Django itself is installed by the cloudharness-django base image as an
    # unpinned `Django>=5`. Pinning it here means the portal runs a known
    # version rather than whatever happened to be current when that image was
    # last built. 6.1 is not reachable yet: both django-ninja and
    # django-prometheus still declare `Django<6.1`.
    "Django==6.0.8",
    "django-import-export==3.3.9",
    "django-ninja==1.6.2",
    "django-prometheus==2.5.0",  # 2.4.1 caps at Django<6.0
    "django-simple-history==3.11.0",
    "gdown==5.2.2",
    "pandas==2.3.3",
    "pillow==12.3.0",
    "psycopg2-binary==2.9.12",
    "sentry-sdk[django]==2.59.0",
    # Security floors for packages the portal never imports itself but pulls
    # in transitively. Each one keeps the resolver away from releases with a
    # known advisory; drop an entry once its parent requires a patched
    # release on its own.
    "filelock>=3.20.3",  # via gdown
    "idna>=3.15",  # via requests
    "requests>=2.33.0",  # via gdown
    "soupsieve>=2.8.4",  # via beautifulsoup4 -> gdown
    "sqlparse>=0.5.4",  # via django
    "urllib3>=2.7.0",  # via requests, sentry-sdk
]

setup(
    name=NAME,
    version=VERSION,
    description="portal",
    author_email="developers@metacell.us",
    url="",
    keywords=["OpenAPI", "portal"],
    install_requires=REQUIRES,
    packages=find_packages(),
    include_package_data=True,
    long_description="Antibody Registry web application",
)
