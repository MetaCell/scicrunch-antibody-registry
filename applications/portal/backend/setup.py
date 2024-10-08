# coding: utf-8

import sys

from setuptools import find_packages, setup

NAME = "portal"
VERSION = "1.0.0"

# To install the library, run the following
#
# python setup.py install
#
# prerequisite: setuptools
# http://pypi.python.org/pypi/setuptools

REQUIRES = [
    "django-import-export>=3.0.1",
    "sentry-sdk[django]",
    "django-simple-history",
    "pandas"
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
