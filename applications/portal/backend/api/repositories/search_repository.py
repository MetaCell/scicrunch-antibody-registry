from typing import List
from functools import reduce
import re

from django.db.models import Q, Transform, CharField, Lookup, F, Func
from django.db.models.functions import Length
from django.db.models.expressions import Value
from django.contrib.postgres.search import SearchVectorField, SearchQuery, SearchVector, SearchHeadline

from ..models import Antibody


# @CharField.register_lookup
# class FtsStartswith(Lookup):
#     lookup_name = 'fts_startswith'

#     def as_sql(self, compiler, connection):
#         lhs, lhs_params = self.process_lhs(compiler, connection)
#         rhs, rhs_params = self.process_rhs(compiler, connection)
#         params = lhs_params + rhs_params
#         return (f"to_tsvector('english', COALESCE({lhs}, '')) @@ "
#                 f"to_tsquery(regexp_replace({rhs}, '[^a-zA-Z0-9]', '', 'g') || ':*')", params)


@CharField.register_lookup
class RemoveComa(Transform):
    lookup_name = 'remove_coma'

    def as_sql(self, compiler, connection):
        lhs, params = compiler.compile(self.lhs)
        return (f"replace({lhs}, ',', '')", params)


def fts_antibodies(page: int = 0, size: int = 50, search: str = '') -> List[Antibody]:
    norm_search = re.sub('[^a-zA-Z0-9]', '', search) + ":*"
    catalog_num_match = (Antibody.objects
                                 .annotate(search=SearchVector('catalog_num__normalize', 'cat_alt__normalize_relaxed', config='english'))
                                 .filter(search=norm_search)
                                 )
    # if we match catalog_num or cat_alt, we return those results without looking for other fields
    # as the match is a perfect match or a prefix match depending on the search word,
    # sorting the normalized catalog_num by length and returning the smallest
    if catalog_num_match.count() > 1:
        return (catalog_num_match.annotate(cat_length=Length('catalog_num__normalize'))
                                 .annotate(alt_length=Length('cat_alt__normalize_relaxed'))
                                 .order_by('cat_length', 'alt_length'))

    # According to https://github.com/MetaCell/scicrunch-antibody-registry/issues/52
    # If the catalog number is not matched, then return records if the query matches any visible or invisible field.
    search_cols = [
        'ab_id',
        'accession',
        'commercial_type',
        'uid',
        'uid_legacy',
        'url',
        'subregion',
        'modifications',
        'epitope',
        'source_organism',
        'clonality',
        'product_isotype',
        'product_conjugate',
        'defining_citation',
        'product_form',
        'comments',
        'applications',
        'kit_contents',
        'feedback',
        'curator_comment',
        'disc_date',
        'status',
    ]
    # In the case that the cat num is not matched,
    # primary ranking:
    # + Additional desirata3: if the name, clone ID, vendor name, match the search string, rank result
    #   higher than other field matches.
    names_search = (Antibody.objects
                            .annotate(search=SearchVector('ab_name',
                                                          'clone_id__normalize_relaxed', config='english'))
                            .filter(search=search)
                            .annotate(nb_citations=Length('defining_citation') - Length('defining_citation__remove_coma'))
                            .annotate(disc_date_len=Length('disc_date')))
    vendor_search = (Antibody.objects
                            .annotate(search=SearchVector('vendor', config='english'))
                            .filter(vendor__name__search=search)
                            .annotate(nb_citations=Length('defining_citation') - Length('defining_citation__remove_coma'))
                            .annotate(disc_date_len=Length('disc_date')))
    top_ranked_search = names_search.union(vendor_search)


    # + Additional desirata: use the number of citations as part of the sorting function
    #   (the higher the citations, the higher the rank)
    # + Additional desirata2: if the record contains string in the "disc_date" field, then downgrade
    #   the result (put on bottom of result set)
    subfields_search = (Antibody.objects
                                .annotate(search=SearchVector(*search_cols, config='english'))
                                .filter(search=search)
                                .annotate(nb_citations=Length('defining_citation') - Length('defining_citation__remove_coma'))
                                .annotate(disc_date_len=Length('disc_date')))

    # index is not used for antigen_search
    # disabled at the moment
    # antigen_search = (Antibody.objects
    #                           .annotate(search=SearchVector('antigen__symbol', config='english'))
    #                           .filter(search=search)
    #                           .annotate(nb_citations=Length('defining_citation') - Length('defining_citation__remove_coma'))
    #                           .annotate(disc_date_len=Length('disc_date')))
    # sub_search = (subfields_search.union(antigen_search)
    #                               .distinct()
    #                               .order_by('nb_citations', 'disc_date_len'))

    # Please bold the match in the search result in each record.
    results = top_ranked_search.union(subfields_search.order_by('nb_citations', 'disc_date_len'))
    import ipdb; ipdb.set_trace()

    return results

def filter_antibodies(page: int = 0, size: int = 50, search: str = '', **kwargs) -> List[Antibody]:
    # todo: implement @afonsobspinto
    for filter in kwargs.values():
        pass
        # todo: append filters to queryset @afonsobspinto
    return []
