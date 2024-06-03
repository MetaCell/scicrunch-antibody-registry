from api.models import Antibody
from api.repositories.filtering_utils import convert_filters_to_q
from .search_repository import apply_plain_sorting, pageitems_if_page_in_bound, MAX_SORTED
from django.core.paginator import Paginator


def plain_filter_antibodies(page: int = 1, size: int = 10, filters=None):
	filtered_antibodies = Antibody.objects.filter(
		convert_filters_to_q(filters)
	).select_related("vendor").prefetch_related("species").prefetch_related("applications").distinct()

	antibodies_count = filtered_antibodies.count()

	if antibodies_count == 0:
		return []
	
	if antibodies_count < MAX_SORTED:
		filtered_antibodies = apply_plain_sorting(
			filtered_antibodies, filters)
		
	p = Paginator(filtered_antibodies, size)
	items = pageitems_if_page_in_bound(page, p)
	return items, antibodies_count
