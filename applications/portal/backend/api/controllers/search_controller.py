from typing import List
from fastapi import HTTPException

from api.services import search_service, antibody_service
from api.services.user_service import UnrecognizedUser, get_current_user_id
from openapi.models import FilterRequest, PaginatedAntibodies
from openapi.models import Antibody as AntibodyDTO


def fts_antibodies(page: int = 1, size: int = 50, search: str = '') -> PaginatedAntibodies:
    if page is None:
        page = 1
    if size is None:
        size = 50
    if page < 1:
        raise HTTPException(status_code=400, detail="Pages start at 1")
    if size < 1:
        raise HTTPException(status_code=400, detail="Size must be greater than 0")
    if page * size > 500:
        try:
            get_current_user_id()
        except UnrecognizedUser:
            raise HTTPException(status_code=401, detail="Request not allowed")
    if search.startswith("AB_"):
        try:
            a = antibody_service.get_antibody(int(search.replace("AB_", "")), accession=int(search.replace("AB_", "")))
            return PaginatedAntibodies(page=int(page), totalElements=len(a), items=a)
        except Exception as e:
            return PaginatedAntibodies(page=int(page), totalElements=0, items=[])
    return search_service.fts_antibodies(page, size, search)


def filter_antibodies(body: FilterRequest) -> PaginatedAntibodies:
    if body.size > 100:
        raise HTTPException(status_code=400, detail="Size must be less than 100")
    return search_service.filter_antibodies(body)
