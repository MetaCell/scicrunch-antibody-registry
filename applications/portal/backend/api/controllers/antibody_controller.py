
from fastapi import HTTPException

from typing import List
import jwt
from api.services import antibody_service

from openapi.models import AddUpdateAntibody as AddUpdateAntibodyDTO
from openapi.models import Antibody as AntibodyDTO

from cloudharness.auth import AuthClient
from cloudharness.middleware import get_authentication_token

def get_antibodies(page: int = 0, size: int = 50) -> List[AntibodyDTO]:
    return antibody_service.get_antibodies(page, size)

def get_user_id():
    token = get_authentication_token()
    try:
        return jwt.decode(token, verify=False, algorithms='RS256')['sub']
    except Exception as e:
        raise HTTPException(status_code=401, detail="Unrecognized user")

def get_user_antibodies(page: int = 0, size: int = 50) -> List[AntibodyDTO]:
    
    return antibody_service.get_user_antibodies(page, size, get_user_id())

def create_antibody(body: AddUpdateAntibodyDTO) -> None:
    try:
        return antibody_service.create_antibody(body, get_user_id())
    except antibody_service.AntibodyDataException as e:
        raise HTTPException(status_code=400, detail=dict(name=e.field_name, value=e.field_value))
    except antibody_service.DuplicatedAntibody as e:
        raise HTTPException(status_code=409, detail="Antibody already exist with this catalog number: %s" % e.ab_id)


def get_antibody(antibody_id: int) -> AntibodyDTO:
    return antibody_service.get_antibody(antibody_id)


def update_antibody(antibody_id: str, body: AddUpdateAntibodyDTO) -> None:
    return antibody_service.update_antibody(antibody_id, body)


def delete_antibody(antibody_id: str) -> None:
    return antibody_service.delete_antibody(antibody_id)
