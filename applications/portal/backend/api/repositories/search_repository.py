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
# One row past MAX_SORTED: enough to tell "exactly MAX_SORTED matches" from
# "more than MAX_SORTED matches", which is all any caller needs. See capped_count.
COUNT_CAP = MAX_SORTED + 1


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


def capped_count(queryset):
    """
    Number of rows in `queryset`, stopping the scan at COUNT_CAP.

    An exact count is the whole cost of a search: to count a full-text match
    Postgres has to visit every matching heap row, and a common term matches
    millions of them (measured on a full-size database: 18s for ~1.6M matches,
    against 40ms for the page of results itself). Nothing downstream can use a
    number larger than the cap -- past MAX_SORTED the results come back
    unranked and the UI renders the total as "10,000+" -- so the count stops
    one row past it and the planner turns it into an early-exit scan.
    """
    return queryset.values("pk")[:COUNT_CAP].count()


def count_is_capped(count):
    """True when `count` hit the cap, i.e. the real total is unknown but larger."""
    return count >= COUNT_CAP


def curated_antibodies_count():
    """Exact number of curated antibodies, from the AntibodyStats cache."""
    # imported lazily: api.services imports the repositories, not the reverse
    from api.services import antibody_service
    return antibody_service.count()


def pageitems_if_page_in_bound(page, p):
    """Return Django model instances directly - Django Ninja handles serialization"""
    if count_is_capped(p.count):
        # num_pages is a floor rather than the real bound when the count was
        # capped, so it cannot be used to reject a page: slice straight into
        # the queryset and let an out-of-range page come back empty on its own.
        first = max(page - 1, 0) * p.per_page  # get_page() treats page < 1 as page 1
        return list(p.object_list[first:first + p.per_page])
    return list(p.get_page(page)) if page <= p.num_pages else []


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
        # no `ranking__gte=MIN_CATALOG_RANKING` here: ts_rank is never negative,
        # so the predicate excluded nothing while forcing the tsvector and its
        # rank to be recomputed for every candidate row -- in the count query
        # too (measured: 22ms against 0.8ms for the same count)
        .filter(search=search_query, status=STATUS.CURATED)
    ).select_related("vendor").prefetch_related("species").prefetch_related("applications")

    # if we match catalog_num or cat_alt, we return those results without looking for other fields
    # as the match is a perfect match or a prefix match depending on the search word,
    # sorting the normalized catalog_num by length and returning the smallest
    catalog_num_match_filtered = catalog_num_match \
        .filter(convert_filters_to_q(filters))

    count = capped_count(catalog_num_match_filtered)

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

    filters_q = convert_filters_to_q(filters)

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
        if filters_q:
            count_base = Antibody.objects.filter(
                antibodysearch__search_vector=search_query, status=STATUS.CURATED)
        else:
            # With nothing to filter on the antibody itself, count on
            # antibody_search alone: it carries its own status column (kept in
            # sync by the migration 0023 triggers) and is a quarter of the size
            # of api_antibody, so the count stops touching the antibody heap
            # just to read a status that eliminates ~9% of the rows. Joining it
            # made Postgres seq-scan all 6GB of api_antibody (measured: 18s
            # against 12s uncapped, 490ms against 56ms for a term under the cap).
            count_base = AntibodySearch.objects.filter(
                search_vector=search_query, status=STATUS.CURATED)

    filtered_antibodies = (
        base_query
        .filter(filters_q)
        .select_related("vendor").prefetch_related("species").prefetch_related("applications")
    )
    count_query = count_base.filter(filters_q)

    if filters_require_distinct(filters):
        filtered_antibodies = filtered_antibodies.distinct()
        count_query = count_query.values("pk").distinct()

    if not search and not filters_q:
        # the unfiltered total is the headline figure on the home page, so it
        # has to stay exact rather than capped -- serve it from the stats cache
        antibodies_count = curated_antibodies_count()
    else:
        antibodies_count = capped_count(count_query)
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
