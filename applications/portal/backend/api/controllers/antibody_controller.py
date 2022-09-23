from fastapi import HTTPException

from typing import List

from api.services import antibody_service

from openapi.models import AddUpdateAntibody as AddUpdateAntibodyDTO
from openapi.models import Antibody as AntibodyDTO


def get_antibodies(page: int = 0, size: int = 50) -> List[AntibodyDTO]:
    return antibody_service.get_antibodies(page, size)


def create_antibody(body: AddUpdateAntibodyDTO) -> None:
    try:
        return antibody_service.create_antibody(body)
    except antibody_service.AntibodyDataException as e:
        raise HTTPException(status_code=400, detail=e.field_name)



def get_antibody(antibody_id: int) -> AntibodyDTO:
    return antibody_service.get_antibody(antibody_id)


def update_antibody(antibody_id: str, body: AddUpdateAntibodyDTO) -> None:
    return antibody_service.update_antibody(antibody_id, body)


def delete_antibody(antibody_id: str) -> None:
    return antibody_service.delete_antibody(antibody_id)
