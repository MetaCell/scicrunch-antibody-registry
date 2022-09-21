from typing import List

from openapi.models import Antibody


def fts_antibodies(page: int = 0, size: int = 50, search: str = '') -> List[Antibody]:
    # todo: implement @afonsobspinto
    offset = page * size
    limit = offset + size
    return Antibody.objects.all()[offset:limit]


def filter_antibodies(page: int = 0, size: int = 50, search: str = '', **kwargs) -> List[Antibody]:
    # todo: implement @afonsobspinto
    for filter in kwargs.values():
        pass
        # todo: append filters to queryset @afonsobspinto
    return []
