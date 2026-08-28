from functools import lru_cache
from typing import List, Tuple

import dateutil
from django.utils.timezone import now, datetime
from api.models import STATUS, Antibody, AntibodyStats
from cloudharness import log
from api.repositories.filtering_utils import convert_filters_to_q
from api.utilities.functions import strip_ab_from_id


def get_antibody_queryset(antibody_id: int, status=STATUS.CURATED, filters=None, accession=None):
    """
    Antibody model instances for an AB id, with the related objects the API
    response schema needs. Endpoints must serialize model instances: the schema
    resolves `url` and `showLink` off the model, and silently returns null for
    both when handed anything else.
    """
    antibody = Antibody.objects.filter(ab_id=antibody_id, status=status).filter(convert_filters_to_q(filters))
    if not antibody.exists() and accession:
        antibody = Antibody.objects.filter(accession=accession, status=status).filter(convert_filters_to_q(filters))
    return antibody.select_related("vendor", "source_organism").prefetch_related("species").prefetch_related("applications")


def antibodies_by_ab_id(ab_id_query: str, page: int = 1, size: int = 10, filters=None) -> Tuple[List[Antibody], int]:
    """
    Antibodies for an "AB_<id>" query, resolved by exact lookup on
    ab_id/accession. Returns (the requested page of matches, total matches).
    """
    try:
        ab_id = int(strip_ab_from_id(ab_id_query))
    except ValueError:  # "AB_" followed by something that is not an id
        return [], 0
    antibodies = list(get_antibody_queryset(ab_id, filters=filters, accession=ab_id))
    first = max(page - 1, 0) * size  # page < 1 is treated as the first page
    return antibodies[first:first + size], len(antibodies)


def delete_antibody(antibody_id: str) -> None:
    return Antibody.objects.delete(ab_id=antibody_id)


def count():
    """
    Get count of CURATED antibodies using cached statistics table.
    Falls back to direct count if stats not available.
    """
    try:
        stats = AntibodyStats.objects.filter(status=STATUS.CURATED).values_list('count', flat=True).first()
        if stats is not None:
            return stats
    except Exception as e:
        log.warning(f"Failed to get count from AntibodyStats, falling back to direct count: {e}")
    
    # Fallback to direct count
    return Antibody.objects.filter(status=STATUS.CURATED).count()

@lru_cache
def last_update(last_date: datetime = None):
    """
    Get the most recent curate_time for CURATED antibodies.
    Uses cached statistics table first, falls back to direct query.
    """
    if last_date is None:
        last_date = now() - dateutil.relativedelta.relativedelta(months=6)
    
    # Try to get from AntibodyStats first
    try:
        stats_last_update = AntibodyStats.objects.filter(status=STATUS.CURATED).values_list('last_update', flat=True).first()
        if stats_last_update is not None and stats_last_update >= last_date:
            return stats_last_update
    except Exception as e:
        log.warning(f"Failed to get last_update from AntibodyStats, falling back to direct query: {e}")
    
    # Fallback to direct query
    try:
        # Use order_by with first() instead of latest() for better index usage
        result = Antibody.objects.filter(
            status=STATUS.CURATED, 
            curate_time__gte=last_date,
            curate_time__isnull=False
        ).order_by('-curate_time').values_list('curate_time', flat=True).first()
        
        if result:
            return result
        # If no recent updates, try earlier period
        return last_update(last_date - dateutil.relativedelta.relativedelta(months=6))
    except Exception as e:
        log.warning(f"Error fetching last_update: {e}")
        return now()


def get_curated_antibodies_ids():
    antibodies_ids = Antibody.objects.filter(status=STATUS.CURATED).values_list(
        "ab_id", flat=True
    )
    return antibodies_ids
