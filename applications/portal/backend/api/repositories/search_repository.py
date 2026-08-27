from typing import List
from functools import reduce
import re
from api.utilities.functions import catalog_number_chunked

from django.conf import settings
from django.db.models import F, Value, QuerySet, FloatField
from django.db.models.functions import Cast, Replace
from django.db import connection
from django.contrib.postgres.search import SearchVectorField, SearchRank, SearchQuery, SearchVector, SearchHeadline, SearchRank
from django.core.paginator import Paginator

from ..models import STATUS, Antibody, AntibodySearch
from .filtering_utils import convert_filters_to_q, filters_require_distinct, order_by_string, status_q
from cloudharness import log

MIN_CATALOG_RANKING = 0.0  # TODO validate the proper ranking value
MAX_SORTED = settings.LIMIT_NUM_RESULTS


class PrecomputedCountPaginator(Paginator):
    """
    Paginator that reuses a count the caller already computed: the default
    Paginator issues its own COUNT query via `num_pages`, which duplicates
    the (potentially expensive) count query on every request.
    """

    def __init__(self, object_list, per_page, count):
        super().__init__(object_list, per_page)
        self.count = count


def flat(l):
    return [item for sublist in l for item in sublist]


def pageitems_if_page_in_bound(page, p):
    """Return Django model instances directly - Django Ninja handles serialization"""
    return list(p.get_page(page)) if page <= p.num_pages else []


def might_be_catalog_number(search: str):
    return bool(search) and any(c for c in search if c.isdigit())


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
        .filter(search=search_query, ranking__gte=MIN_CATALOG_RANKING, status=STATUS.CURATED)
    ).select_related("vendor").prefetch_related("species").prefetch_related("applications")

    # if we match catalog_num or cat_alt, we return those results without looking for other fields
    # as the match is a perfect match or a prefix match depending on the search word,
    # sorting the normalized catalog_num by length and returning the smallest
    catalog_num_match_filtered = catalog_num_match \
        .filter(convert_filters_to_q(filters))

    count = catalog_num_match_filtered.count()

    if count < MAX_SORTED:
        catalog_num_match_filtered = apply_fts_sorting(
            catalog_num_match_filtered, filters)

    p = PrecomputedCountPaginator(catalog_num_match_filtered, size, count)
    items = pageitems_if_page_in_bound(page, p)
    return items, count


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
        if cat_search[0]:
            return cat_search

    return fts_and_filter_search(page, size, search, filters)


def apply_fts_sorting(filtered_antibodies: QuerySet, filters):
    """
    Search ranking
    1. ranking
    2. defining_citation: oldest citations go first
    3. disc: if the record contains string in the "disc_date" field, then downgrade the result (put on bottom of result set)
    """
    explicit_order_by = order_by_string(filters)
    if explicit_order_by:
        return filtered_antibodies.order_by(*explicit_order_by)
    return filtered_antibodies.annotate(
        ix_float=Cast("ix", FloatField()),
        sorting=F("ranking") - F("antibodysearch__defining_citation") / 1000 - F("antibodysearch__disc") * 100 + F("ix_float") / 1000000
    ).order_by('-sorting')


def apply_plain_sorting(filtered_antibodies: QuerySet, filters):
    """
    If sorting is not specified, we sort by the order of the ids
    """
    explicit_order_by = order_by_string(filters)
    if explicit_order_by:
        return filtered_antibodies.order_by(*explicit_order_by)
    return filtered_antibodies.order_by('-ix')


def fts_and_filter_search(page: int = 0, size: int = 10, search: str = '', filters=None):
    """
    if search doesn't exist, then we do: filtering + sorting
    If search exists, then we do:
        if under the limit: fts + filtering + sorting (sort by rank and then by sort model in FE)
        if over the limit: fts + filtering 
    """
    # According to https://github.com/MetaCell/scicrunch-antibody-registry/issues/52
    # If the catalog number is not matched, then return records if the query matches any visible or invisible field.
    # highlight_cols = flat((F(f), Value(' ')) for f in search_col_names)[:-1]

    if not search:
        base_query = Antibody.objects.filter(status=STATUS.CURATED)
        count_base = base_query
    else:
        search_query = SearchQuery(search)
        ranking = SearchRank(F("antibodysearch__search_vector"), search_query)
        base_query = Antibody.objects.annotate(ranking=ranking)\
            .filter(antibodysearch__search_vector=search_query, status=STATUS.CURATED)
        # count on a queryset without the ranking annotation: combined with
        # DISTINCT, the annotation forces ts_rank() to be computed per row
        # inside the COUNT subquery
        count_base = Antibody.objects.filter(
            antibodysearch__search_vector=search_query, status=STATUS.CURATED)

    filters_q = convert_filters_to_q(filters)
    filtered_antibodies = (
        base_query
        .filter(filters_q)
        .select_related("vendor").prefetch_related("species").prefetch_related("applications")
    )
    count_query = count_base.filter(filters_q)

    if filters_require_distinct(filters):
        filtered_antibodies = filtered_antibodies.distinct()
        count_query = count_query.values("pk").distinct()

    antibodies_count = count_query.count()
    if antibodies_count == 0:
        return [], 0

    if antibodies_count < MAX_SORTED:
        if search:
            # /*/ 100 + F("disc_date") + 1000
            filtered_antibodies = apply_fts_sorting(
                filtered_antibodies, filters)
        else:
            filtered_antibodies = apply_plain_sorting(
                filtered_antibodies, filters)

    p = PrecomputedCountPaginator(filtered_antibodies, size, antibodies_count)
    items = pageitems_if_page_in_bound(page, p)
    return items, antibodies_count
