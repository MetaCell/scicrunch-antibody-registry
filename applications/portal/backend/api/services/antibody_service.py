import re
from datetime import datetime
from typing import List

import dateutil
from django.core.paginator import Paginator

from api.mappers.antibody_mapper import AntibodyMapper
from api.models import STATUS, Antibody
from api.utilities.exceptions import DuplicatedAntibody
from openapi.models import AddUpdateAntibody as AddUpdateAntibodyDTO
from openapi.models import Antibody as AntibodyDTO, PaginatedAntibodies

antibody_mapper = AntibodyMapper()


def search_antibodies_by_catalog(search: str, page: int = 1, size: int = 50,
                                 status=STATUS.CURATED) -> PaginatedAntibodies:
    p = Paginator(Antibody.objects.select_related("antigen", "vendor", "source_organism").prefetch_related(
        "species").all().filter(
        status=status, catalog_num__iregex=".*" + re.sub('[^0-9a-zA-Z]+', '.*', search) + ".*").order_by("-ix"), size)
    items = [antibody_mapper.to_dto(ab) for ab in p.get_page(page)]
    return PaginatedAntibodies(page=int(page), totalElements=p.count, items=items)


def get_antibodies(page: int = 1, size: int = 50) -> PaginatedAntibodies:
    p = Paginator(Antibody.objects.select_related("antigen", "vendor", "source_organism").
                  prefetch_related("species").all()
                  .filter(status=STATUS.CURATED).order_by("-ix"), size)
    items = [antibody_mapper.to_dto(ab) for ab in p.get_page(page)]
    return PaginatedAntibodies(page=int(page), totalElements=p.count, items=items)


def get_user_antibodies(userid: str, page: int = 1, size: int = 50) -> PaginatedAntibodies:
    p = Paginator(Antibody.objects.all().filter(
        uid=userid).order_by("lastedit_time"), size)
    items = [antibody_mapper.to_dto(ab) for ab in p.get_page(page)]
    return PaginatedAntibodies(page=int(page), totalElements=p.count, items=items)


def create_antibody(body: AddUpdateAntibodyDTO, userid: str) -> AntibodyDTO:
    antibody = antibody_mapper.from_dto(body)
    antibody.uid = userid
    antibody.save()

    if antibody.get_duplicate():
        raise DuplicatedAntibody(antibody_mapper.to_dto(antibody))

    return antibody_mapper.to_dto(antibody)


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
        return Antibody.objects.all().filter(status=STATUS.CURATED, curate_time__gte=last_date) \
            .latest("curate_time").curate_time
    except Antibody.DoesNotExist:
        return Antibody.objects.all().filter(status=STATUS.CURATED).latest("curate_time").curate_time
