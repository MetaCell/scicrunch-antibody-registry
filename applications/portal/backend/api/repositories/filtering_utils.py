from django.db.models import Q
from ninja.errors import HttpError
from portal.constants import FILTERABLE_AND_SORTABLE_FIELDS, FOREIGN_OR_M2M_FIELDS, M2M_FIELDS
from api.schemas import FilterRequest, SortOrderEnum
from api.models import STATUS
from api.services.user_service import get_current_user_id


def filter_and_sort_keys(filters):
    """Every antibody field name referenced by a filter request."""
    keys = []
    for key_value_filters in (filters.contains, filters.equals, filters.starts_with,
                              filters.ends_with, filters.is_any_of):
        if key_value_filters:
            keys.extend(f.key for f in key_value_filters)
    keys.extend(filters.is_empty or [])
    keys.extend(filters.is_not_empty or [])
    if filters.sort_on:
        keys.extend(column.key for column in filters.sort_on)
    return keys


def check_filters_are_valid(filters):
    # Django Ninja/Pydantic validates types and structure, but not the field
    # names: an unknown key would reach the ORM and raise a FieldError, which
    # surfaces as a 500 rather than a bad request
    if not isinstance(filters, FilterRequest):
        return False

    return all(key in FILTERABLE_AND_SORTABLE_FIELDS
               for key in filter_and_sort_keys(filters))


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


def filters_require_distinct(filters):
    """
    DISTINCT is only needed when a filter or sort key spans a many-to-many
    relationship, whose join duplicates antibody rows. Applying it
    unconditionally forces COUNT/SELECT queries to deduplicate over every
    column, which is very expensive (see ANTIBODY-REGISTRY-5F).
    """
    if not filters or not isinstance(filters, FilterRequest):
        return False
    return any(key in M2M_FIELDS for key in filter_and_sort_keys(filters))


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
    
    # if is_user_scope is true, then we filter by the owning user
    if filters.is_user_scope:
        if user is not None and not user.is_anonymous:
            query["owner"] = user
        else:
            # Fallback to JWT decoding if user context is not available
            from cloudharness_django.services.user import get_user_by_kc_id
            resolved = get_user_by_kc_id(get_current_user_id())
            if resolved is None:
                # never filter owner=None: it would leak all ownerless rows
                raise HttpError(401, "Unrecognized user")
            query["owner"] = resolved

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
