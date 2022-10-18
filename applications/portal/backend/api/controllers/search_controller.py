from typing import List

from api.services import search_service, antibody_service
from openapi.models import FilterRequest, PaginatedAntibodies
from openapi.models import Antibody as AntibodyDTO


def fts_antibodies(page: int = 1, size: int = 50, search: str = '') -> PaginatedAntibodies:
    # return antibody_service.search_antibodies_by_catalog(search, page, size) # TODO temporary search, TBR
    return search_service.fts_antibodies(page, size, search)


def filter_antibodies(body: FilterRequest) -> PaginatedAntibodies:
    return search_service.filter_antibodies(body)
