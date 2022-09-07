from typing import List

from api.services import search_service
from openapi.models import FilterRequest
from openapi.models import Antibody as AntibodyDTO


def fts_antibodies(page: int = 0, size: int = 50, search: str = '') -> List[AntibodyDTO]:
    return search_service.fts_antibodies(page, size, search)


def filter_antibodies(body: FilterRequest) -> List[AntibodyDTO]:
    return search_service.filter_antibodies(body)
