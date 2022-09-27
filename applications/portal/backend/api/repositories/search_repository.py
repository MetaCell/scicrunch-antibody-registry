from typing import List

from django.db.models import Q, Transform, CharField, Lookup, F, Func
from django.db.models.functions import Length
from django.db.models.expressions import Value
from django.contrib.postgres.search import SearchVectorField, SearchQuery

from openapi.models import Antibody as AntibodyDTO
from ..models import Antibody


@CharField.register_lookup
class IStartswith(Lookup):
    lookup_name = 'ftsistartswith'

    def as_sql(self, compiler, connection):
        lhs, lhs_params = self.process_lhs(compiler, connection)
        rhs, rhs_params = self.process_rhs(compiler, connection)
        params = lhs_params + rhs_params
        return (f"to_tsvector('english', COALESCE({lhs}, '')) @@ "
                f"to_tsquery(UPPER(regexp_replace({rhs}, '[^a-zA-Z0-9]', '', 'g')) || ':*')", params)


def fts_antibodies(page: int = 0, size: int = 50, search: str = '') -> List[Antibody]:
    catalog_num_match = Antibody.objects.filter(catalog_num__normalize__ftsistartswith=search)
    cat_alt_prefix_match = Antibody.objects.filter(cat_alt__normalize_relaxed__comma_split__ftsistartswith=search)
    full_cat_match = catalog_num_match.union(cat_alt_prefix_match)
    if full_cat_match.count() > 1:
        return catalog_num_match
    return []


def filter_antibodies(page: int = 0, size: int = 50, search: str = '', **kwargs) -> List[Antibody]:
    # todo: implement @afonsobspinto
    for filter in kwargs.values():
        pass
        # todo: append filters to queryset @afonsobspinto
    return []
