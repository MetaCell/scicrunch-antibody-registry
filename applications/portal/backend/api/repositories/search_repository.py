from typing import List
from functools import reduce
import re
from api.utilities.functions import catalog_number_chunked

from django.conf import settings
from django.db.models import F, Value
from django.db import connection
from django.contrib.postgres.search import SearchVectorField, SearchRank, SearchQuery, SearchVector, SearchHeadline, SearchRank

from ..models import STATUS, Antibody, AntibodySearch
from cloudharness import log

MIN_CATALOG_RANKING = 0.0  # TODO validate the proper ranking value
MAX_SEARCH_RESULTS = settings.LIMIT_NUM_RESULTS

def flat(l):
    return [item for sublist in l for item in sublist]


def fts_by_catalog_number(search: str, page, size):
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
    count = catalog_num_match.count()
    offset = (page - 1) * size
    if count > settings.LIMIT_NUM_RESULTS:
        
        return catalog_num_match[offset: size + offset], count
    elif count:
        return catalog_num_match.order_by('-ranking')[offset: size + offset], count
    return None

def might_be_catalog_number(search: str):
    return any(c for c in search if c.isdigit())

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

    if might_be_catalog_number(search):
        cat_search = fts_by_catalog_number(re.sub(r'[^\w\s]', '', search), page, size)

        if cat_search:
            return cat_search
    
    return fts_others_search(page, size, search)
    
    


def fts_others_search(page: int = 0, size: int = settings.LIMIT_NUM_RESULTS, search: str = ''):
    search_query = SearchQuery(search)
    # According to https://github.com/MetaCell/scicrunch-antibody-registry/issues/52
    # If the catalog number is not matched, then return records if the query matches any visible or invisible field.

    ranking = SearchRank(F("search_vector"), search_query)

    # highlight_cols = flat((F(f), Value(' ')) for f in search_col_names)[:-1]

    offset = (page - 1) * size
    subfields_search = AntibodySearch.objects.annotate(
        ranking=ranking,
    ).filter(search_vector=search_query, status=STATUS.CURATED)

    count = subfields_search.count()

    if count == 0:
        return [], 0

    if count > settings.LIMIT_NUM_RESULTS:
        ids = [a.ix for a  in subfields_search.filter(disc_date__isnull=True)[offset: size + offset]]
        return Antibody.objects.filter(ix__in=ids, disc_date__isnull=True).select_related('vendor'), count
    
    def sort_fn(x: AntibodySearch):
        ranking = -x.ranking
        if x.defining_citation:
            try:
                ranking -= float(x.defining_citation.replace(",", "")) / 100
            except ValueError:
                log.warning("Invalid citation value: %s", x.defining_citation)
                ranking -= 1
        
        if x.disc_date:
            ranking += 1000
        return ranking
    
    ids = [a.ix for a in sorted((a for a  in subfields_search),key=sort_fn)][offset: size + offset]
    id_map = {ids[i]:i for i in range(len(ids))}
    # the second sorting is needed because the query doesn't keep the ids order. 
    return sorted(Antibody.objects.filter(ix__in=ids).select_related('vendor'),key=lambda x:id_map[x.ix]), count



