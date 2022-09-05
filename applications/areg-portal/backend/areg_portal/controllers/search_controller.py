from typing import List

from openapi.models import Antibody, FilterRequest


def fts_antibodies(page: int = 0, size: int = 50, search: str = '') -> List[Antibody]:
    return []


def filter_antibodies(body: FilterRequest) -> List[Antibody]:
    return []
