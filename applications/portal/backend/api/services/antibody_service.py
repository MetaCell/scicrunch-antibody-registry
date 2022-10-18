from datetime import datetime
import re
from typing import List
import dateutil

from django.core.paginator import Paginator

from cloudharness import log

from api.models import STATUS, Antibody
from api.mappers.antibody_mapper import AntibodyMapper, AntibodyDataException
from openapi.models import Antibody as AntibodyDTO, PaginatedAntibodies
from openapi.models import AddUpdateAntibody as AddUpdateAntibodyDTO

magic = 64544


class DuplicatedAntibody(Exception):
    def __init__(self, ab_id):
        super().__init__("Antibody exists")
        self.ab_id = ab_id


antibody_mapper = AntibodyMapper()

def search_antibodies_by_catalog(search: str, page: int = 1, size: int = 50, status=STATUS.CURATED) -> PaginatedAntibodies:
    p = Paginator(Antibody.objects.select_related("antigen", "vendor", "source_organism").prefetch_related("species").all().filter(
        status=status, catalog_num__iregex=".*" + re.sub('[^0-9a-zA-Z]+', '.*', search) + ".*").order_by("-ix"), size)
    items = [antibody_mapper.to_dto(ab) for ab in p.get_page(page)]
    return PaginatedAntibodies(page=int(page), totalElements=p.count, items=items)

def get_antibodies(page: int = 1, size: int = 50) -> PaginatedAntibodies:
    p = Paginator(Antibody.objects.select_related("antigen", "vendor", "source_organism").prefetch_related("species").all().filter(
        status=STATUS.CURATED).order_by("-ix"), size)
    items = [antibody_mapper.to_dto(ab) for ab in p.get_page(page)]
    return PaginatedAntibodies(page=int(page), totalElements=p.count, items=items)


def get_user_antibodies(userid: str, page: int = 1, size: int = 50) -> PaginatedAntibodies:
    p = Paginator(Antibody.objects.all().filter(uid=userid), size)
    items = [antibody_mapper.to_dto(ab) for ab in p.get_page(page)]
    return PaginatedAntibodies(page=int(page), totalElements=p.count, items=items)


def generate_id(antibody: Antibody):
    return antibody.ix + magic


def create_antibody(body: AddUpdateAntibodyDTO, userid: str) -> AntibodyDTO:

    try:
        ab: Antibody = Antibody.objects.get(
            vendor__name=body.vendorName, catalog_num=body.catalogNum)
        raise DuplicatedAntibody(ab.ab_id)
    except Antibody.DoesNotExist:
        antibody = antibody_mapper.from_dto(body)
        antibody.ab_id = generate_id(antibody)
        antibody.accession = antibody.ab_id
        antibody.uid = userid
        antibody.status = STATUS.QUEUE
        antibody.save()
        return antibody_mapper.to_dto(antibody)
    except Antibody.MultipleObjectsReturned:
        log.warn("Unexpectedly found multiple antibodies with catalog number %s and vendor %s",
                 body.vendorName, body.catalogNum)
        raise DuplicatedAntibody(", ". join(str(a.ab_id) for a in Antibody.objects.all(
        ).filter(vendor__name=body.vendorName, catalog_num=body.catalogNum)))


def get_antibody(antibody_id: int, status=STATUS.CURATED) -> List[AntibodyDTO]:
    try:
        return [antibody_mapper.to_dto(a) for a in Antibody.objects.all().filter(ab_id=antibody_id, status=status)]
    except Antibody.DoesNotExist:
        return None


def update_antibody(antibody_id: str, body: AddUpdateAntibodyDTO) -> AntibodyDTO:
    antibody_mapper = AntibodyMapper()
    try:
        current_antibody = Antibody.objects.get(
            id=int(antibody_id.split("AB_")[1]))
        new_ab = antibody_mapper.from_dto(body)

        # TODO: update current_antibody with new_antibody data @afonsobspinto
        return current_antibody
    except Antibody.DoesNotExist:
        return None

    # return antibody_repository.update_or_create(current_antibody)


def delete_antibody(antibody_id: str) -> None:
    return Antibody.objects.delete(ab_id=antibody_id)


def count():
    return Antibody.objects.all().filter(status=STATUS.CURATED).count()


def last_update():
    # Used to improve performance -- otherwise need to sort all antibodies!
    last_date = datetime.now() - dateutil.relativedelta.relativedelta(months=6)
    try:
        return Antibody.objects.all().filter(status=STATUS.CURATED, curate_time__gte=last_date).latest("curate_time").curate_time
    except Antibody.DoesNotExist:
        return Antibody.objects.all().filter(status=STATUS.CURATED).latest("curate_time").curate_time
