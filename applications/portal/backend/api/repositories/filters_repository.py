
from django.db.models import Q
from openapi.models import Sortorder
from fastapi import HTTPException
from portal.constants import FILTERABLE_FIELDS
from openapi.models import Operation, SearchCriteriaOptions
from api.services.user_service import get_current_user_id

FILTER_TYPES = {filter_type.value for filter_type in SearchCriteriaOptions}

def check_filters_are_valid(filters):
	for filter_type, filter_values in dict(filters).items():
		if filter_type not in FILTER_TYPES:
			return False

		if filter_type == SearchCriteriaOptions.page.value or filter_type == SearchCriteriaOptions.size.value:
			if not isinstance(filter_values, int):
				return False
		elif filter_type == SearchCriteriaOptions.search.value:
			if not isinstance(filter_values, str):
				return False
		elif filter_type == SearchCriteriaOptions.isUserScope.value:
			if not isinstance(filter_values, bool):
				return False
		elif filter_type == SearchCriteriaOptions.operation.value:
			if filter_values not in [Operation.and_, Operation.or_]:
				return False
		elif filter_type == SearchCriteriaOptions.isEmpty.value or filter_type == SearchCriteriaOptions.isNotEmpty.value:
			if not isinstance(filter_values, list):
				return False
			
			for filter_value in filter_values:
				if filter_value not in FILTERABLE_FIELDS:
					return False
		else:
			if not isinstance(filter_values, list):
				return False
			
			for filter_value in filter_values:
				if filter_value.key not in FILTERABLE_FIELDS:
					return False

	return True

def lookup_spanning_relationships_string(fieldname):
	"""
		Search allows:
		Foreign key fields - vendors
		ManyToMany fields - applications, species
	"""
	if fieldname in ["vendor", "application", "species"]:
		return f"{fieldname}__name"
	else:
		return fieldname

def convert_filters_to_q(filters):
	query = {}
	if not filters:
		return Q()
	if (not check_filters_are_valid(filters)):
		raise HTTPException(status_code=400, detail="Invalid filters")
	
	# First for loop is limited to filters operation types size = 7. T.C. O(7n) = O(n), 
	# where n is the number of columns in a particular filter type. 
	for filter_type, filter_values in dict(filters).items():
		# if filter_type == "contains":
		if filter_type == SearchCriteriaOptions.contains.value:
			for filter_value in filter_values:
				query[f"{lookup_spanning_relationships_string(filter_value.key)}__icontains"] = filter_value.value
		elif filter_type == SearchCriteriaOptions.equals.value:
			for filter_value in filter_values:
				query[f"{lookup_spanning_relationships_string(filter_value.key)}__iexact"] = filter_value.value
		elif filter_type == SearchCriteriaOptions.startsWith.value:
			for filter_value in filter_values:
				query[f"{lookup_spanning_relationships_string(filter_value.key)}__istartswith"] = filter_value.value
		elif filter_type == SearchCriteriaOptions.endsWith.value:
			for filter_value in filter_values:
				query[f"{lookup_spanning_relationships_string(filter_value.key)}__iendswith"] = filter_value.value
		elif filter_type == SearchCriteriaOptions.isEmpty.value:
			for filter_value in filter_values:
				query[f"{lookup_spanning_relationships_string(filter_value)}__isnull"] = True
		elif filter_type == SearchCriteriaOptions.isNotEmpty.value:
			for filter_value in filter_values:
				query[f"{lookup_spanning_relationships_string(filter_value)}__isnull"] = False
		elif filter_type == SearchCriteriaOptions.isAnyOf.value:
			for filter_value in filter_values:
				query[f"{lookup_spanning_relationships_string(filter_value.key)}__in"] = filter_value.value
		# if isUserScope is true, then we filter by userid
		elif filter_type == SearchCriteriaOptions.isUserScope.value and filter_values == True:
			user_id = get_current_user_id()
			query["uid"] = user_id
		else:
			pass

	return Q(**query) if query else Q()


def order_by_string(filters):
	if filters.sortOn is None or len(filters.sortOn) == 0:
		return []
	order_by_string = []
	for column in filters.sortOn:
		order_by_string.append(f"{'-' if column.sortorder == Sortorder.desc else ''}{column.key}")
	return order_by_string
