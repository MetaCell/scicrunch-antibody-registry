from typing import List

from api.repositories import search_repository
from openapi.models import FilterRequest
from openapi.models import Antibody as AntibodyDTO


def fts_antibodies(page: int = 0, size: int = 50, search: str = '') -> List[AntibodyDTO]:
    return search_repository.fts_antibodies()


def filter_antibodies(body: FilterRequest) -> List[AntibodyDTO]:
    return search_repository.filter_antibodies()
