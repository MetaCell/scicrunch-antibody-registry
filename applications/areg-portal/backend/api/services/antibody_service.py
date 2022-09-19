from typing import List

from api.models import Antibody

from api.mappers.antibody_mapper import AntibodyMapper
from api.repositories import antibody_repository
from openapi.models import Antibody as AntibodyDTO
from openapi.models import AddUpdateAntibody as AddUpdateAntibodyDTO


def get_antibodies(page: int = 0, size: int = 50) -> List[AntibodyDTO]:
    antibody_mapper = AntibodyMapper()
    antibodies_daos = antibody_repository.get_all(page, size)
    return [antibody_mapper.to_dto(dao) for dao in antibodies_daos]

def generate_id(antibody: Antibody):
    # TODO add logic to generate the AB_ID
    import random
    return random.randint(0, 99999999)

def create_antibody(body: AddUpdateAntibodyDTO) -> None:
    antibody_mapper = AntibodyMapper()
    antibody = antibody_mapper.from_dto(body)
    antibody.ab_id = generate_id(antibody)
    # antibody.ab_id = "AB_%s" % antibody.id
    # TODO add logic to map the vendor to the url

    # TODO add default values (e.g. curation state)
    return antibody_mapper.to_dto(antibody_repository.update_or_create(antibody))


def get_antibody(antibody_id: str) -> AntibodyDTO:
    return antibody_repository.get(antibody_id)


def update_antibody(antibody_id: str, body: AddUpdateAntibodyDTO) -> None:
    antibody_mapper = AntibodyMapper()
    current_antibody = antibody_repository.get(antibody_id)
    new_antibody = antibody_mapper.from_dto(body)
    # todo: update current_antibody with new_antibody data @afonsobspinto
    # return antibody_repository.update_or_create(current_antibody)


def delete_antibody(antibody_id: str) -> None:
    return antibody_repository.delete(antibody_id)
