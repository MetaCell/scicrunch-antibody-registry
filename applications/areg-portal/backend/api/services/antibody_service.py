from typing import List


from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from api.models import Antibody
from api.mappers.antibody_mapper import AntibodyMapper
from openapi.models import Antibody as AntibodyDTO, PaginatedAntibodies
from openapi.models import AddUpdateAntibody as AddUpdateAntibodyDTO


antibody_mapper = AntibodyMapper()

def get_antibodies(page: int = 0, size: int = 50) -> PaginatedAntibodies:
    p = Paginator(Antibody.objects.all(), size)
    items = [antibody_mapper.to_dto(ab) for ab in p.get_page(page)]
    return PaginatedAntibodies(page=int(page), totalElements=p.count, items=items)

def generate_id(antibody: Antibody):
    # TODO add logic to generate the AB_ID https://github.com/MetaCell/scicrunch-antibody-registry/issues/43
    import random
    return random.randint(0, 99999999)

def create_antibody(body: AddUpdateAntibodyDTO) -> AntibodyDTO:
    
    antibody = antibody_mapper.from_dto(body)
    antibody.ab_id = generate_id(antibody)
    # antibody.ab_id = "AB_%s" % antibody.id
    # TODO add logic to map the vendor to the url

    # TODO add default values (e.g. curation state)
    antibody.save()
    return antibody_mapper.to_dto(antibody)


def get_antibody(antibody_id: int) -> AntibodyDTO:
    try:
        return antibody_mapper.to_dto(Antibody.objects.get(ab_id=antibody_id))
    except Antibody.DoesNotExist:
        return None


def update_antibody(antibody_id: str, body: AddUpdateAntibodyDTO) -> AntibodyDTO:
    antibody_mapper = AntibodyMapper()
    try:
        current_antibody = Antibody.objects.get(id=int(antibody_id.split("AB_")[1]))
        new_ab = antibody_mapper.from_dto(body)
        
        # TODO: update current_antibody with new_antibody data @afonsobspinto
        return current_antibody
    except Antibody.DoesNotExist:
        return None
    
    # return antibody_repository.update_or_create(current_antibody)


def delete_antibody(antibody_id: str) -> None:
    return antibody_repository.delete(antibody_id)
