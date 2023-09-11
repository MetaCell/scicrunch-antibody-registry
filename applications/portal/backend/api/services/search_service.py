from typing import List
from api.utilities.functions import strip_ab_from_id

from django.core.paginator import Paginator

from api.repositories import search_repository
from openapi.models import FilterRequest
from openapi.models import Antibody as AntibodyDTO, PaginatedAntibodies
from ..mappers.antibody_mapper import AntibodyMapper
from . import antibody_service

antibody_mapper = AntibodyMapper()


def fts_antibodies(page: int = 1, size: int = 50, search: str = '') -> List[AntibodyDTO]:
    page = page or 0  # required at the moment, issue with default values in main.py-L134
    size = size or 50  # required at the moment, issue with default values in main.py-L134
    if "AB_" in search:
        if search.startswith("RRID:"):
            search = search.replace("RRID:", "").strip()
        antibodies = antibody_service.get_antibody(strip_ab_from_id(search))
        if antibodies:
            return PaginatedAntibodies(page=int(page), totalElements=len(antibodies), items=antibodies)
    antibodies_res, count = search_repository.fts_antibodies(page=page, size=size, search=search)
    antibodies = [antibody_mapper.to_dto(a) for a in antibodies_res]
    return PaginatedAntibodies(page=int(page), totalElements=count, items=antibodies)


def filter_antibodies(body: FilterRequest) -> List[AntibodyDTO]:
    return search_repository.filter_antibodies()
