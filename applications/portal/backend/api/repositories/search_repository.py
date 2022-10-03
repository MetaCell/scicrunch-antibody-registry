from typing import List
from functools import reduce
import re

from django.db.models import F, Value
from django.db.models.functions import Length, Concat, Coalesce
from django.db.models.expressions import Value
from django.contrib.postgres.search import SearchVectorField, SearchQuery, SearchVector, SearchHeadline, SearchRank

from ..models import Antibody


def flat(l):
    return [item for sublist in l for item in sublist]


def fts_antibodies(page: int = 0, size: int = 50, search: str = '') -> List[Antibody]:
    # preparing two search terms, one for catalog_num, the other for normal search.
    norm_search = re.sub('[^a-zA-Z0-9]', '', search) + ":*"
    search = ' & '.join(c + ':*' for c in search.split(' ') if c)
    norm_search_query = SearchQuery(norm_search, search_type='raw')
    search_query = SearchQuery(search, search_type='raw')
    norm_or_search = search_query | norm_search_query

    catalog_num_match = (Antibody.objects
                                 .annotate(search=SearchVector('catalog_num__normalize', 'cat_alt__normalize_relaxed', config='english'))
                                 .filter(search=norm_search_query)
                                 )
    # if we match catalog_num or cat_alt, we return those results without looking for other fields
    # as the match is a perfect match or a prefix match depending on the search word,
    # sorting the normalized catalog_num by length and returning the smallest
    if catalog_num_match.count() >= 1:
        return (catalog_num_match.annotate(cat_length=Length('catalog_num__normalize'))
                                 .annotate(alt_length=Length('cat_alt__normalize_relaxed'))
                                 .order_by('cat_length', 'alt_length'))

    # According to https://github.com/MetaCell/scicrunch-antibody-registry/issues/52
    # If the catalog number is not matched, then return records if the query matches any visible or invisible field.
    first_cols = SearchVector('ab_name',
                              'clone_id__normalize_relaxed', config='english', weight='A')
    search_col_names = [
        'accession',
        'commercial_type',
        'uid',
        'uid_legacy',
        'url',
        'subregion',
        'modifications',
        'epitope',
        'clonality',
        'product_isotype',
        'product_conjugate',
        'defining_citation',
        'product_form',
        'comments',
        'kit_contents',
        'feedback',
        'curator_comment',
        'disc_date',
        'status',
    ]
    search_cols = SearchVector(*search_col_names, config='english', weight='C')

    # In the case that the cat num is not matched,
    # primary ranking:
    # + Additional desirata3: if the name, clone ID, vendor name, match the search string, rank result
    #   higher than other field matches.
    nb_citation_rank = Length(Coalesce('defining_citation', Value(''))) - Length(Coalesce('defining_citation__remove_coma', Value('')))
    ranking = nb_citation_rank - (100 + Length(Coalesce('disc_date', Value(''))))

    highlight_cols = flat((F(f), Value(' ')) for f in search_col_names)[:-1]

    subfields_search = (Antibody.objects
                                .annotate(
                                    rank=SearchRank(first_cols + search_cols, norm_or_search),
                                    search=first_cols + search_cols,
                                    nb_citations=nb_citation_rank,
                                    # headline=SearchHeadline(
                                    #     Concat(*highlight_cols),
                                    #     search_query,
                                    #     highlight_all=True
                                    # )
                                )
                                .filter(search=norm_or_search, rank__gte=0.3)
                                # .order_by('-rank')
                                )

    subfields_search2 = (Antibody.objects
                                .annotate(
                                    search=first_cols + search_cols,
                                    # nb_citations=nb_citation_rank,
                                    ranking=ranking,
                                    # headline=SearchHeadline(
                                    #     Concat(*highlight_cols),
                                    #     search_query,
                                    #     highlight_all=True
                                    # )
                                )
                                .filter(search=norm_or_search)
                                .order_by('-ranking')
                                )

    # vendor_search = (Antibody.objects
    #                         .annotate(search=SearchVector('vendor', config='english'))  # trick to use the index
    #                         .filter(vendor__name__search=search_query)
    #                         .annotate(nb_citations=nb_citation_rank)
    #                         # .annotate(headline=SearchHeadline(
    #                         #     'vendor__name',
    #                         #     search_query,
    #                         #     highlight_all=True
    #                         # ))
    #                         )
    # top_ranked_search = names_search.union(vendor_search)
    # if top_ranked_search.count() > 1000:
    #     # currently, if there is more than 1000 results, we directly return them
    #     # as they are supposed to be ranked first. It doesn't make sense to search
    #     # over the rest of the DB entries in this case.
    #     return top_ranked_search.order_by('-nb_citations')

    # + Additional desirata: use the number of citations as part of the sorting function
    #   (the higher the citations, the higher the rank)
    # + Additional desirata2: if the record contains string in the "disc_date" field, then downgrade
    #   the result (put on bottom of result set)



    # subfields_search = (Antibody.objects
    #                             .annotate(search=search_cols)
    #                             .filter(search=search_query)
    #                             .annotate(nb_citations=nb_citation_rank)
    #                             # .annotate(headline=SearchHeadline(
    #                             #     Concat(*highlight_cols),
    #                             #     search_query,
    #                             #     highlight_all=True
    #                             # ))
    #                             )

    # index is not used for antigen_search
    # disabled at the moment
    # antigen_search = (Antibody.objects
    #                           .annotate(search=SearchVector('antigen__symbol', config='english'))
    #                           .filter(search=search)
    #                           .annotate(nb_citations=Length('defining_citation') - Length('defining_citation__remove_coma'))
    # sub_search = (subfields_search.union(antigen_search)
    #                               .distinct()
    #                               .order_by('nb_citations', 'disc_date'))

    # Please bold the match in the search result in each record.
    # results = top_ranked_search.union(subfields_search.order_by('-nb_citations', '-disc_date'))
    return subfields_search2


def filter_antibodies(page: int = 0, size: int = 50, search: str = '', **kwargs) -> List[Antibody]:
    # todo: implement @afonsobspinto
    for filter in kwargs.values():
        pass
        # todo: append filters to queryset @afonsobspinto
    return []
