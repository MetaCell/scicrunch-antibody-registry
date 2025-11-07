"""
Search Router - Handles search and filter endpoints
"""
from typing import List, Optional

from ninja import Router
from ninja.errors import HttpError
from django.http import HttpRequest
from django.core.paginator import Paginator

from api.schemas import (
    FilterRequest,
    PaginatedAntibodies,
    VendorSchema,
)
from api.helpers import CamelCaseRouter
from api.models import Application, Specie, Vendor
from api.repositories import search_repository, filter_repository
from api.repositories.filtering_utils import is_user_scoped
from api.services import antibody_service

router = CamelCaseRouter()


@router.get("/fts-antibodies", response=PaginatedAntibodies, tags=["search"])
def fts_antibodies(
    request: HttpRequest,
    q: str,
    page: Optional[int] = None,
    size: Optional[int] = None,
):
    """Search antibodies (Full Text Search)"""
    if page is None:
        page = 1
    if size is None:
        size = 50
    if page < 1:
        raise HttpError(400, "Pages start at 1")
    if size < 1:
        raise HttpError(400, "Size must be greater than 0")
    if page * size > 500:
        if request.user.is_anonymous:
            if request.user.is_anonymous:
                raise HttpError(401, "Request not allowed")
    if q.startswith("AB_"):
        try:
            ab_id = int(q.replace("AB_", ""))
            antibodies = antibody_service.get_antibody(ab_id, accession=ab_id)
            return dict(page=int(page), totalElements=len(antibodies), items=antibodies)
        except Exception as e:
            return dict(page=int(page), totalElements=0, items=[])
    
    from api.services.search_service import fts_antibodies
    antibodies, count = fts_antibodies(page, size, q)
    return dict(page=int(page), totalElements=count, items=antibodies)


@router.post("/search/antibodies", response=PaginatedAntibodies, tags=["search"])
def filter_antibodies(request: HttpRequest, body: FilterRequest):
    """Search on Antibodies with custom filters"""
    if body.size and body.size > 100:
        raise HttpError(400, "Size must be less than 100")
    
    from api.services.search_service import filter_antibodies as search_filter_antibodies
    
    antibodies, count = search_filter_antibodies(body, request.user)
    
    return dict(page=int(body.page), totalElements=count, items=antibodies)





@router.get("/species", response=List[str], tags=["search"])
def get_species(request: HttpRequest):
    """Get all species"""
    species = Specie.objects.all().order_by("name")
    return [s.name for s in species]


@router.get("/applications", response=List[str], tags=["search"])
def get_applications(request: HttpRequest):
    """Get all applications"""
    applications = Application.objects.all().order_by("name")
    return [a.name for a in applications]


@router.get("/vendors", response=List[VendorSchema], tags=["search"])
def get_vendors(request: HttpRequest):
    """Get all vendors"""
    vendors = Vendor.objects.all().order_by("name")
    return list(vendors)
