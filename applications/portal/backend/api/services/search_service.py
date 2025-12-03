from typing import List, Tuple
from api.utilities.functions import strip_ab_from_id

from django.core.paginator import Paginator

from api.repositories import search_repository
from api.models import Antibody
from api.repositories import filter_repository
from api.repositories.filtering_utils import is_user_scoped


def fts_antibodies(page: int = 1, size: int = 10, search: str = '', filters=None) -> Tuple[List[Antibody], int]:
    """Return (antibodies, total_count) tuple for Django Ninja to handle serialization"""
    page = page or 1
    size = size or 10
    return fts_and_filter_antibodies(page=page, size=size, search=search, filters=filters)


def filter_antibodies(filter_request, user=None) -> Tuple[List[Antibody], int]:
    """Return (antibodies, total_count) tuple for Django Ninja to handle serialization"""
    if (is_user_scoped(filter_request)):  # user's antibodies - plain filter without fts
        return plain_filter_antibodies(page=filter_request.page, size=filter_request.size, filters=filter_request, user=user)
    return fts_and_filter_antibodies(page=filter_request.page, size=filter_request.size, search=filter_request.search, filters=filter_request)


def fts_and_filter_antibodies(page: int = 1, size: int = 10, search: str = '', filters=None) -> Tuple[List[Antibody], int]:
    """Return (antibodies, total_count) tuple for Django Ninja to handle serialization"""
    if "AB_" in search:
        if search.startswith("RRID:"):
            search = search.replace("RRID:", "").strip()
        from . import antibody_service
        antibodies = antibody_service.get_antibody(strip_ab_from_id(search), filters=filters, accession=strip_ab_from_id(search))
        if antibodies:
            # antibody_service returns DTOs, but we need Django models for AB_ search too
            # For now, let's fall through to regular search since AB_ search is handled in the router
            pass

    return search_repository.fts_and_filter_antibodies(page=page, size=size, search=search, filters=filters)


def plain_filter_antibodies(page: int = 1, size: int = 10, filters=None, user=None) -> Tuple[List[Antibody], int]:
    """Return (antibodies, total_count) tuple for Django Ninja to handle serialization"""
    return filter_repository.plain_filter_antibodies(page=page, size=size, filters=filters, user=user)
