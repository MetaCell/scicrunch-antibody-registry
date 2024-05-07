from typing import List
from api.utilities.functions import strip_ab_from_id

from django.core.paginator import Paginator

from api.repositories import search_repository
from openapi.models import FilterRequest
from openapi.models import Antibody as AntibodyDTO, PaginatedAntibodies
from . import antibody_service



def fts_antibodies(page: int = 1, size: int = 10, search: str = '', filters=None) -> List[AntibodyDTO]:
    page = page or 0  # required at the moment, issue with default values in main.py-L134
    size = size or 10  # required at the moment, issue with default values in main.py-L134
    return fts_and_filter_antibodies(page=page, size=size, search=search, filters=filters)
    
def filter_antibodies(filter_request: FilterRequest) -> List[AntibodyDTO]:
    return fts_and_filter_antibodies(page=filter_request.page, size=filter_request.size, search=filter_request.search, filters=filter_request)


def fts_and_filter_antibodies(page: int = 1, size: int = 10, search: str = '', filters=None) -> List[AntibodyDTO]:
    if "AB_" in search:
        if search.startswith("RRID:"):
            search = search.replace("RRID:", "").strip()
        antibodies = antibody_service.get_antibody(strip_ab_from_id(search), filters=filters, accession=strip_ab_from_id(search))
        if antibodies:
            return PaginatedAntibodies(page=int(page), totalElements=len(antibodies), items=antibodies)
        
    antibodies, count = search_repository.fts_and_filter_antibodies(page=page, size=size, search=search, filters=filters)
    return PaginatedAntibodies(page=int(page), totalElements=count, items=antibodies)

