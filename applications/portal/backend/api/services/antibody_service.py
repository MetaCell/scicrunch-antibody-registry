
from functools import lru_cache
from typing import List

import dateutil
from django.core.paginator import Paginator
from django.utils.timezone import now, datetime
from django.db.models import F
from api.mappers.antibody_mapper import AntibodyMapper
from api.models import STATUS, Antibody, AntibodyStats, CommercialType
from api.utilities.exceptions import DuplicatedAntibody, AntibodyDataException
from cloudharness import log
from openapi.models import AddAntibody as AddAntibodyDTO
from openapi.models import UpdateAntibody as UpdateAntibodyDTO, AntibodyStatusEnum
from openapi.models import Antibody as AntibodyDTO, PaginatedAntibodies
from api.utilities.functions import check_if_status_exists_or_curated
from api.repositories.filtering_utils import convert_filters_to_q
from api.utilities.cache import ttl_cache

antibody_mapper = AntibodyMapper()

@lru_cache
def get_antibodies(page: int = 1, size: int = 10, date_from: datetime = None, date_to: datetime = None, status: str = None) -> PaginatedAntibodies:
    try:
        query = Antibody.objects.filter(status=check_if_status_exists_or_curated(status))
        if date_from:
            query = query.filter(lastedit_time__gte=date_from)
        if date_to:
            query = query.filter(lastedit_time__lte=date_to)

        p = Paginator(query.select_related("vendor", "source_organism").prefetch_related("species").prefetch_related("applications").order_by("-ix"), size)
        items = [antibody_mapper.to_dto(ab) for ab in p.get_page(page)]

    except Antibody.DoesNotExist:
        return PaginatedAntibodies(page=int(page), totalElements=0, items=[])
    return PaginatedAntibodies(page=int(page), totalElements=p.count, items=items)

def get_user_antibodies(userid: str, page: int = 1, size: int = 10) -> PaginatedAntibodies:
    p = Paginator(Antibody.objects.filter(
        uid=userid).order_by("-ix"), size)
    items = [antibody_mapper.to_dto(ab) for ab in p.get_page(page)]
    return PaginatedAntibodies(page=int(page), totalElements=p.count, items=items)


def create_antibody(body: AddAntibodyDTO, userid: str) -> AntibodyDTO:
    antibody = antibody_mapper.from_dto(body)
    antibody.uid = userid
    antibody.save()

    if antibody.accession != antibody.ab_id:
        raise DuplicatedAntibody(antibody_mapper.to_dto(antibody))

    return antibody_mapper.to_dto(antibody)


def get_antibody(antibody_id: int, status=STATUS.CURATED, filters=None, accession=None) -> List[AntibodyDTO]:
    try:
        antibody = Antibody.objects.filter(ab_id=antibody_id, status=status).filter(convert_filters_to_q(filters))
        if not antibody.exists() and accession:
            antibody = Antibody.objects.filter(accession=accession, status=status).filter(convert_filters_to_q(filters))
        antibody = antibody.select_related("vendor", "source_organism").prefetch_related("species").prefetch_related("applications")
        return [antibody_mapper.to_dto(a) for a in antibody]
    except Antibody.DoesNotExist:
        return None


def get_antibody_by_accession(accession: int) -> List[AntibodyDTO]:
    try:
        return antibody_mapper.to_dto(
            Antibody.objects.select_related("vendor", "source_organism")
            .prefetch_related("species")
            .prefetch_related("applications")
            .get(accession=accession)
        )
    except Antibody.DoesNotExist:
        raise
    except Antibody.MultipleObjectsReturned:
        log.warning(f"Multiple antibodies with accession {accession}")
        raise


def update_antibody(user_id: str, antibody_accession_number: str, body: UpdateAntibodyDTO) -> AntibodyDTO:
    if getattr(body, 'vendorName', None) is not None:
        raise AntibodyDataException(
            "Vendor name cannot be updated", 'vendorName', None)
    if getattr(body, 'catalogNum', None) is not None:
        raise AntibodyDataException(
            "Catalog number cannot be updated", 'catalogNum', None)
    current_antibody = Antibody.objects.get(
        accession=antibody_accession_number, uid=user_id)
    updated_antibody = antibody_mapper.from_dto(AntibodyDTO(**body.__dict__, abId=current_antibody.ab_id,
                                                            ix=current_antibody.ix,
                                                            catalogNum=current_antibody.catalog_num,
                                                            vendorName=current_antibody.vendor.name,
                                                            insertTime=current_antibody.insert_time))
    updated_antibody.status = STATUS.QUEUE
    updated_antibody.save()
    return antibody_mapper.to_dto(updated_antibody)


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
