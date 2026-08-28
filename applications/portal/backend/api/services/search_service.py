from typing import List, Tuple

from api.repositories import search_repository
from api.models import Antibody
from api.repositories import filter_repository
from api.repositories.filtering_utils import is_user_scoped
from api.services import antibody_service
from api.utilities.functions import prefix as AB_ID_PREFIX

RRID_PREFIX = "RRID:"


def search_antibodies(page: int = 1, size: int = 10, search: str = '', filters=None) -> Tuple[List[Antibody], int]:
    """
    Entry point for a search box query. An AB id -- on its own or pasted as a
    whole RRID -- names one record and is resolved by exact lookup; anything
    else is full text search.

    Returns an (antibodies, total_count) tuple for Django Ninja to serialize.
    """
    page = page or 1
    size = size or 10
    search = (search or '').strip()  # filter-only requests carry no search term
    if search.startswith(RRID_PREFIX):
        search = search[len(RRID_PREFIX):].strip()
    if search.startswith(AB_ID_PREFIX):
        return antibody_service.antibodies_by_ab_id(search, page=page, size=size, filters=filters)
    return fts_and_filter_antibodies(page=page, size=size, search=search, filters=filters)


def filter_antibodies(filter_request, user=None) -> Tuple[List[Antibody], int]:
    """Return (antibodies, total_count) tuple for Django Ninja to handle serialization"""
    if (is_user_scoped(filter_request)):  # user's antibodies - plain filter without fts
        return plain_filter_antibodies(page=filter_request.page, size=filter_request.size, filters=filter_request, user=user)
    return search_antibodies(page=filter_request.page, size=filter_request.size, search=filter_request.search, filters=filter_request)


def fts_and_filter_antibodies(page: int = 1, size: int = 10, search: str = '', filters=None) -> Tuple[List[Antibody], int]:
    """Full text search over antibodies, with the request filters applied"""
    return search_repository.fts_and_filter_antibodies(page=page, size=size, search=search, filters=filters)


def plain_filter_antibodies(page: int = 1, size: int = 10, filters=None, user=None) -> Tuple[List[Antibody], int]:
    """Return (antibodies, total_count) tuple for Django Ninja to handle serialization"""
    return filter_repository.plain_filter_antibodies(page=page, size=size, filters=filters, user=user)
