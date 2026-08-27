from api.models import Antibody
from api.repositories.filtering_utils import convert_filters_to_q, filters_require_distinct
from .search_repository import apply_plain_sorting, pageitems_if_page_in_bound, MAX_SORTED, PrecomputedCountPaginator


def plain_filter_antibodies(page: int = 1, size: int = 10, filters=None, user=None):
    filtered_antibodies = (
        Antibody.objects.filter(
            convert_filters_to_q(filters, user)
        ).select_related("vendor").prefetch_related("species").prefetch_related("applications")
        .with_curated_vendor_domains()
    )

    if filters_require_distinct(filters):
        filtered_antibodies = filtered_antibodies.distinct()
        antibodies_count = filtered_antibodies.values("pk").count()
    else:
        antibodies_count = filtered_antibodies.count()

    if antibodies_count == 0:
        return [], antibodies_count

    if antibodies_count < MAX_SORTED:
        filtered_antibodies = apply_plain_sorting(
            filtered_antibodies, filters)

    p = PrecomputedCountPaginator(filtered_antibodies, size, antibodies_count)
    items = pageitems_if_page_in_bound(page, p)
    return items, antibodies_count
