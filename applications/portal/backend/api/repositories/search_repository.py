from typing import List
from functools import reduce
import re
from api.utilities.functions import catalog_number_chunked

from django.conf import settings
from django.db.models import F, Value
from django.db.models.functions import Length, Concat, Coalesce
from django.contrib.postgres.search import SearchVectorField, SearchRank, SearchQuery, SearchVector, SearchHeadline, SearchRank

from ..models import STATUS, Antibody

MIN_CATALOG_RANKING = 0.0  # TODO validate the proper ranking value


def flat(l):
    return [item for sublist in l for item in sublist]


def fts_by_catalog_number(search: str):
    search = catalog_number_chunked(search, fill=" & ")

    search_query = SearchQuery(search, search_type='raw')

    vector = SearchVector('catalog_num_search', config='simple')
    catalog_num_match = (
        Antibody.objects.annotate(
            search=vector,
            ranking=SearchRank(vector, search_query, normalization=Value(1)))
        .filter(search=search_query, status=STATUS.CURATED, ranking__gte=MIN_CATALOG_RANKING)
    )
    # if we match catalog_num or cat_alt, we return those results without looking for other fields
    # as the match is a perfect match or a prefix match depending on the search word,
    # sorting the normalized catalog_num by length and returning the smallest
    if catalog_num_match.count() >= 1:
        return catalog_num_match.order_by('-ranking')
    return None


def fts_antibodies(page: int = 0, size: int = settings.LIMIT_NUM_RESULTS, search: str = '') -> List[Antibody]:
    # According to https://github.com/MetaCell/scicrunch-antibody-registry/issues/52
    # Match the calalog number (make sure to treat the cat_alt field the same way)
    # If the catalog number is not matched, then return records if the query matches any visible or invisible field.
    #
    # In the case that the cat num is not matched,
    # primary ranking:
    # + Additional desirata3: if the name, clone ID, vendor name, match the search string, rank result
    #   higher than other field matches.
    # + Additional desirata: use the number of citations as part of the sorting function
    #   (the higher the citations, the higher the rank)
    # + Additional desirata2: if the record contains string in the "disc_date" field, then downgrade
    #   the result (put on bottom of result set)

    # preparing two search terms, one for catalog_num, the other for normal search.

    # search only allows alphanumeric characters and spaces
    search = re.sub(r'[^\w\s]', '', search)
    cat_search = fts_by_catalog_number(search)

    if cat_search:
        return cat_search

    search_query = SearchQuery(" & ".join(search.split()), search_type='raw')
    # According to https://github.com/MetaCell/scicrunch-antibody-registry/issues/52
    # If the catalog number is not matched, then return records if the query matches any visible or invisible field.
    first_cols = SearchVector(
        'ab_name', 'clone_id__normalize_relaxed', config='english', weight='A')

    search_col_names = [
        'accession',
        'subregion',
        'modifications',
        'epitope',
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
        'vendor__name',
        'antigen__symbol',
        'source_organism__name',
    ]
    search_cols = SearchVector(*search_col_names, config='english', weight='C')

    # In the case that the cat num is not matched,
    # primary ranking:
    # + Additional desirata3: if the name, clone ID, vendor name, match the search string, rank result
    #   higher than other field matches.
    nb_citation_rank = Length(Coalesce('defining_citation', Value(
        ''))) - Length(Coalesce('defining_citation__remove_coma', Value('')))

    ranking = SearchRank(first_cols, search_query) + \
        SearchRank(search_cols, search_query) + nb_citation_rank

    highlight_cols = flat((F(f), Value(' ')) for f in search_col_names)[:-1]

    offset = (page - 1 ) * size
    subfields_search = Antibody.objects.annotate(
        search=first_cols + search_cols,
    ).filter(search=search_query, status=STATUS.CURATED)[offset: size + offset]

    count = subfields_search.count()
    if count == size:
        return subfields_search.select_related('vendor')
    # min_rank = 0.03
    # while subfields_search.count() >= settings.LIMIT_NUM_RESULTS:
    #     # too many results --> return the first settings.LIMIT_NUM_RESULTS without sorting/ranking
    #     subfields_search = subfields_search.filter(ranking_gte=min_rank)
    #     min_rank *= 2

    if count == 0:
        return []

    # lets apply the ranking
    subfields_search = Antibody.objects.annotate(
        search=first_cols + search_cols,
        nb_citations=nb_citation_rank,
        ranking=ranking,
    ).filter(search=search_query, status=STATUS.CURATED).order_by('-ranking')[offset: size + offset].select_related('vendor')
                        

    return subfields_search

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
