from typing import List, Union
from api.models import Antibody

import jwt
from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from api.services import antibody_service
from api.utilities.exceptions import AntibodyDataException
from cloudharness.middleware import get_authentication_token
from openapi.models import AddAntibody as AddAntibodyDTO, PaginatedAntibodies
from openapi.models import UpdateAntibody as UpdateAntibodyDTO
from openapi.models import Antibody as AntibodyDTO


def get_antibodies(page: int = 0, size: int = 50) -> PaginatedAntibodies:
    return antibody_service.get_antibodies(page, size)


def get_user_id() -> str:
    token = get_authentication_token()
    try:
        return jwt.decode(token, options={"verify_signature": False}, algorithms='RS256')['sub']
    except Exception as e:
        raise HTTPException(status_code=401, detail="Unrecognized user")


def get_user_antibodies(page: int = 1, size: int = 50) -> PaginatedAntibodies:
    return antibody_service.get_user_antibodies(get_user_id(), page, size)


def create_antibody(body: AddAntibodyDTO) -> Union[AntibodyDTO, JSONResponse]:
    try:
        return antibody_service.create_antibody(body, get_user_id())
    except AntibodyDataException as e:
        raise HTTPException(status_code=400, detail=dict(
            name=e.field_name, value=e.field_value))
    except antibody_service.DuplicatedAntibody as e:
        return JSONResponse(status_code=409, content=jsonable_encoder(e.antibody))


def get_antibody(antibody_id: int) -> List[AntibodyDTO]:
    return antibody_service.get_antibody(antibody_id)


def update_user_antibody(accession_number: str, body: UpdateAntibodyDTO) -> AntibodyDTO:
    try:
        return antibody_service.update_antibody(get_user_id(), accession_number, body)
    except AntibodyDataException as e:
        raise HTTPException(status_code=400, detail=dict(
            name=e.field_name, value=e.field_value))


def delete_antibody(antibody_id: str) -> None:
    return antibody_service.delete_antibody(antibody_id)

def get_by_accession(accession_number: int) -> AntibodyDTO:
    try:
        return antibody_service.get_antibody_by_accession(accession_number)
    except Antibody.DoesNotExist as e:
        raise HTTPException(status_code=404, detail=e.message)
