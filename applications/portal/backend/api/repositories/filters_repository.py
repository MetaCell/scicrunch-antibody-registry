
from django.db.models import Q

def convert_filters_to_q(filters):
	query = {}
	if not filters:
		return Q()
	for filter_type, filter_values in dict(filters).items():
		if filter_type == "contains":
			for filter_value in filter_values:
				query[f"{filter_value.key}__icontains"] = filter_value.value
		elif filter_type == "equals":
			for filter_value in filter_values:
				query[f"{filter_value.key}__iexact"] = filter_value.value
		elif filter_type == "startsWith":
			for filter_value in filter_values:
				query[f"{filter_value.key}__istartswith"] = filter_value.value
		elif filter_type == "endsWith":
			for filter_value in filter_values:
				query[f"{filter_value.key}__iendswith"] = filter_value.value
		elif filter_type == "isEmpty":
			for filter_value in filter_values:
				query[f"{filter_value}__isnull"] = True
		elif filter_type == "isNotEmpty":
			for filter_value in filter_values:
				query[f"{filter_value}__isnull"] = False
		elif filter_type == "isAnyOf":
			for filter_value in filter_values:
				query[f"{filter_value.key}__in"] = filter_value.value
		else:
			pass

	return Q(**query) if query else Q()
