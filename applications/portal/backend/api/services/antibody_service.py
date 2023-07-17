import re
from datetime import datetime
from typing import List

import dateutil
from django.core.paginator import Paginator

from api.mappers.antibody_mapper import AntibodyMapper
from api.models import STATUS, Antibody, CommercialType
from api.utilities.exceptions import DuplicatedAntibody, AntibodyDataException
from api.utilities.functions import generate_id_aux, strip_ab_from_id
from cloudharness import log
from openapi.models import AddAntibody as AddAntibodyDTO
from openapi.models import UpdateAntibody as UpdateAntibodyDTO
from openapi.models import Antibody as AntibodyDTO, PaginatedAntibodies

antibody_mapper = AntibodyMapper()


def search_antibodies_by_catalog(search: str, page: int = 1, size: int = 50,
                                 status=STATUS.CURATED) -> PaginatedAntibodies:
    p = Paginator(Antibody.objects.select_related("vendor", "source_organism").prefetch_related(
        "species").all().filter(
        status=status, catalog_num__iregex=".*" + re.sub('[^0-9a-zA-Z]+', '.*', search) + ".*").order_by("-ix"), size)
    items = [antibody_mapper.to_dto(ab) for ab in p.get_page(page)]
    return PaginatedAntibodies(page=int(page), totalElements=p.count, items=items)


def get_antibodies(page: int = 1, size: int = 50) -> PaginatedAntibodies:
    try:
        p = Paginator(Antibody.objects.select_related("vendor", "source_organism").
                    prefetch_related("species")
                    .filter(status=STATUS.CURATED).order_by("-ix"), size)
        items = [antibody_mapper.to_dto(ab) for ab in p.get_page(page)]
    except Antibody.DoesNotExist:
        return PaginatedAntibodies(page=int(page), totalElements=0, items=[])
    return PaginatedAntibodies(page=int(page), totalElements=p.count, items=items)


def get_user_antibodies(userid: str, page: int = 1, size: int = 50) -> PaginatedAntibodies:
    p = Paginator(Antibody.objects.filter(
        uid=userid).order_by("-ix"), size)
    items = [antibody_mapper.to_dto(ab) for ab in p.get_page(page)]
    return PaginatedAntibodies(page=int(page), totalElements=p.count, items=items)


def create_antibody(body: AddAntibodyDTO, userid: str) -> AntibodyDTO:
    antibody = antibody_mapper.from_dto(body)
    antibody.uid = userid
    antibody.save()

    if antibody.get_duplicate():
        raise DuplicatedAntibody(antibody_mapper.to_dto(antibody))

    return antibody_mapper.to_dto(antibody)


def get_antibody(antibody_id: int, status=STATUS.CURATED) -> List[AntibodyDTO]:
    try:
        return [antibody_mapper.to_dto(a) for a in Antibody.objects.filter(ab_id=antibody_id, status=status)]
    except Antibody.DoesNotExist:
        return None


def get_antibody_by_accession(accession: int) -> List[AntibodyDTO]:
    try:
        return antibody_mapper.to_dto(Antibody.objects.get(accession=accession))
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
                                                            catalogNum=current_antibody.catalog_num,
                                                            vendorName=current_antibody.vendor.name,
                                                            insertTime=current_antibody.insert_time))
    updated_antibody.save()
    return antibody_mapper.to_dto(updated_antibody)


def delete_antibody(antibody_id: str) -> None:
    return Antibody.objects.delete(ab_id=antibody_id)


def count():
    return Antibody.objects.all().filter(status=STATUS.CURATED).count()


def last_update():
    # Used to improve performance -- otherwise need to sort all antibodies!
    last_date = datetime.now() - dateutil.relativedelta.relativedelta(months=6)
    try:
        return Antibody.objects.filter(status=STATUS.CURATED, curate_time__gte=last_date) \
            .latest("curate_time").curate_time
    except Antibody.DoesNotExist:
        try:
            return Antibody.objects.filter(status=STATUS.CURATED).latest("curate_time").curate_time
        except Antibody.DoesNotExist:
            return datetime.now()
