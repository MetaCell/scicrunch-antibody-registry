from typing import List
from functools import reduce
import re
from api.utilities.functions import catalog_number_chunked

from django.conf import settings
from django.db.models import F, Value
from django.db import connection
from django.contrib.postgres.search import SearchVectorField, SearchRank, SearchQuery, SearchVector, SearchHeadline, SearchRank
from django.core.paginator import Paginator

from ..models import STATUS, Antibody, AntibodySearch
from .filters_repository import convert_filters_to_q, order_by_string
from cloudharness import log
from ..mappers.antibody_mapper import AntibodyMapper

MIN_CATALOG_RANKING = 0.0  # TODO validate the proper ranking value
MAX_SEARCH_RESULTS = settings.LIMIT_NUM_RESULTS

antibody_mapper = AntibodyMapper()

def flat(l):
    return [item for sublist in l for item in sublist]

def pageitems_if_page_in_bound(page, p):
    return [antibody_mapper.to_dto(ab) for ab in p.get_page(page)] if page <= p.num_pages else []

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


def might_be_catalog_number(search: str):
    return any(c for c in search if c.isdigit())


def fts_by_catalog_number(search: str, page, size, filters=None):
    """
        Catalog is part of search and it exists, hence it will definitely do fts. 
        We do filtering if filters are present.
        We do sorting only when the count is under the limit.
    """
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
    catalog_num_match_filtered = catalog_num_match.filter(convert_filters_to_q(filters))
    count = catalog_num_match_filtered.count()

    if count > settings.LIMIT_NUM_RESULTS:
        p = Paginator(catalog_num_match_filtered, size)
        items = pageitems_if_page_in_bound(page, p)
        return items, count
    elif count:
        p = Paginator(catalog_num_match_filtered.order_by(
                *order_by_string(filters)
            ).order_by('-ranking'), size)
        items = pageitems_if_page_in_bound(page, p)
        return items, count
    return None


def fts_and_filter_antibodies(page: int = 0, size: int = 10, search: str = '', filters=None) -> List[Antibody]:
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
        cat_search = fts_by_catalog_number(search, page, size, filters)
        if cat_search:
            return cat_search

    return fts_and_filter_search(page, size, search, filters)


def fts_and_filter_search(page: int = 0, size: int = 10, search: str = '', filters=None):
    """
    if search doesn't exist, then we do: filtering + sorting
    If search exists, then we do:
        if under the limit: fts + filtering + sorting (sort by rank and then by sort model in FE)
        if over the limit: fts + filtering 
    """

    if not search:
        return antibodies_with_pure_filtering_without_fts(filters, page, size)

    search_query = SearchQuery(search)
    # According to https://github.com/MetaCell/scicrunch-antibody-registry/issues/52
    # If the catalog number is not matched, then return records if the query matches any visible or invisible field.
    # highlight_cols = flat((F(f), Value(' ')) for f in search_col_names)[:-1]

    ranking = SearchRank(F("search_vector"), search_query)

    subfields_search = AntibodySearch.objects.annotate(
        ranking=ranking,
    ).filter(search_vector=search_query, status=STATUS.CURATED)

    subfields_search_count = subfields_search.count()
    if subfields_search_count == 0:
        return [], 0

    if subfields_search_count > settings.LIMIT_NUM_RESULTS:
        return antibodies_fts_and_filtering_above_limit(subfields_search, page, size, filters)

    return antibodies_fts_and_filtering_below_limit(subfields_search, page, size, filters)


def antibodies_with_pure_filtering_without_fts(filters, page, size):
    filtered_antibody = Antibody.objects.filter(
        status=STATUS.CURATED
    ).filter(convert_filters_to_q(filters)).select_related("vendor").prefetch_related("species")
    filtered_and_sorted_antibody = filtered_antibody.order_by(*order_by_string(filters))
    p = Paginator(filtered_and_sorted_antibody, size)
    items = pageitems_if_page_in_bound(page, p)
    return items, filtered_and_sorted_antibody.count()


def antibodies_fts_and_filtering_above_limit(subfields_search, page, size, filters):
    ids = [a.ix for a in subfields_search.filter(disc_date__isnull=True)]
    filtered_antibodies = Antibody.objects.filter(ix__in=ids, disc_date__isnull=True).filter(
        convert_filters_to_q(filters)
    ).select_related("vendor").prefetch_related("species")

    filtered_antibodies = sort_by_sortmodel_if_antibodies_count_below_limit(filtered_antibodies, filters)

    p = Paginator(filtered_antibodies, size)
    items = pageitems_if_page_in_bound(page, p)
    return items, filtered_antibodies.count()


def antibodies_fts_and_filtering_below_limit(subfields_search, page, size, filters):
    ids = [a.ix for a in sorted((a for a  in subfields_search),key=sort_fn)]
    id_map = {ids[i]:i for i in range(len(ids))}
    filtered_antibodies = (
        Antibody.objects.filter(ix__in=ids)
        .select_related("vendor")
        .prefetch_related("species")
        .filter(convert_filters_to_q(filters))
    )

    filtered_antibodies = sort_by_sortmodel_if_antibodies_count_below_limit(filtered_antibodies, filters)

    count = filtered_antibodies.count()
    # if sorting is not specified, we sort by the order of the ids
    if not order_by_string(filters):
        filtered_antibodies = sorted(
            filtered_antibodies, 
            key=lambda x:id_map[x.ix]
        )
    p = Paginator(filtered_antibodies, size)
    items = pageitems_if_page_in_bound(page, p)
    return items, count


def sort_by_sortmodel_if_antibodies_count_below_limit(filtered_antibodies, filters):
    if filtered_antibodies.count() < settings.LIMIT_NUM_RESULTS:
        filtered_antibodies = filtered_antibodies.order_by(*order_by_string(filters))
    return filtered_antibodies
