from django.db.models import Q
from ninja.errors import HttpError
from portal.constants import FILTERABLE_AND_SORTABLE_FIELDS, FOREIGN_OR_M2M_FIELDS
from api.schemas import FilterRequest, SortOrderEnum
from api.models import STATUS
from api.services.user_service import get_current_user_id


def check_filters_are_valid(filters):
    # Django Ninja FilterRequest schema validation - simplified version
    # Since Django Ninja already handles field validation via Pydantic, we just need basic checks
    if not isinstance(filters, FilterRequest):
        return False
    
    # Basic validation - Django Ninja schema ensures correct types and structure
    return True


def lookup_spanning_relationships_string(fieldname):
    """
                Search allows:
                Foreign key fields - vendors
                ManyToMany fields - applications, species
        """
    if fieldname in FOREIGN_OR_M2M_FIELDS:
        return f"{fieldname}__name"
    else:
        return fieldname


def convert_filters_to_q(filters, user=None):
    query = {}
    if not filters:
        return Q()
    if (not check_filters_are_valid(filters)):
        raise HttpError(400, "Invalid filters")

    # Django Ninja schema uses snake_case field names, process them directly
    if filters.contains:
        for filter_value in filters.contains:
            query[f"{lookup_spanning_relationships_string(filter_value.key)}__icontains"] = filter_value.value
    
    if filters.equals:
        for filter_value in filters.equals:
            query[f"{lookup_spanning_relationships_string(filter_value.key)}__iexact"] = filter_value.value
    
    if filters.starts_with:
        for filter_value in filters.starts_with:
            query[f"{lookup_spanning_relationships_string(filter_value.key)}__istartswith"] = filter_value.value
    
    if filters.ends_with:
        for filter_value in filters.ends_with:
            query[f"{lookup_spanning_relationships_string(filter_value.key)}__iendswith"] = filter_value.value
    
    if filters.is_empty:
        for filter_value in filters.is_empty:
            query[f"{lookup_spanning_relationships_string(filter_value)}__isnull"] = True
    
    if filters.is_not_empty:
        for filter_value in filters.is_not_empty:
            query[f"{lookup_spanning_relationships_string(filter_value)}__isnull"] = False
    
    if filters.is_any_of:
        for filter_value in filters.is_any_of:
            query[f"{lookup_spanning_relationships_string(filter_value.key)}__in"] = filter_value.value
    
    # if is_user_scope is true, then we filter by userid
    if filters.is_user_scope:
        if user and hasattr(user, 'member'):
            user_id = user.member.kc_id
            query["uid"] = user_id
        else:
            # Fallback to JWT decoding if user context is not available
            user_id = get_current_user_id()
            query["uid"] = user_id

    return Q(**query) if query else Q()


def order_by_string(filters):
    if (not filters) or (not filters.sort_on):
        return []
    order_by = []
    for column in filters.sort_on:
        order_by.append(f"{'-' if column.sortorder == SortOrderEnum.desc else ''}{column.key}")
    return order_by


def is_user_scoped(filters):
    if not filters or not isinstance(filters, FilterRequest):
        return False
    if filters.is_user_scope == True:
        return True
    return False


def status_q(filters):
    if is_user_scoped(filters):
        return Q()  # if user scoped, return all antibodies for the user
    return Q(status=STATUS.CURATED)
