from datetime import datetime
from typing import List, Union, Optional
import os

from cloudharness import log
from api.models import Antibody, STATUS
from api.services.user_service import UnrecognizedUser, get_current_user_id, check_if_user_is_admin

from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse, RedirectResponse

from api.services import antibody_service, filesystem_service
from api.utilities.exceptions import AntibodyDataException

from openapi.models import AddAntibody as AddAntibodyDTO, PaginatedAntibodies
from openapi.models import UpdateAntibody as UpdateAntibodyDTO
from openapi.models import Antibody as AntibodyDTO
from openapi.models import AntibodyStatusEnum

def get_antibodies(page: int, size: int, updated_from: datetime, updated_to: datetime, status=str) -> PaginatedAntibodies:
    if page is None:
        page = 1
    if size is None:
        size = 50
    if page < 1:
        raise HTTPException(status_code=400, detail="Pages start at 1")
    if size < 1:
        raise HTTPException(status_code=400, detail="Size must be greater than 0")
    if page * size > 500:
        try:
            get_current_user_id()
        except UnrecognizedUser:
            raise HTTPException(status_code=401, detail="Request not allowed")
    try:
        return antibody_service.get_antibodies(int(page), int(size), updated_from, updated_to, status)
    except ValueError:
        raise HTTPException(status_code=400, detail="Page and size must be integers")


def get_user_id() -> str:
    try:
        return get_current_user_id()
    except UnrecognizedUser:
        raise HTTPException(status_code=401, detail="Unrecognized user")


def get_user_antibodies(page: int = 1, size: int = 50) -> PaginatedAntibodies:
    if page < 1:
        raise HTTPException(status_code=400, detail="Pages start at 1")
    if size < 1:
        raise HTTPException(status_code=400, detail="Size must be greater than 0")
    if size > 100:
        raise HTTPException(status_code=400, detail="Size must be less than 100")
    return antibody_service.get_user_antibodies(get_current_user_id(), page, size)


def create_antibody(body: AddAntibodyDTO) -> Union[AntibodyDTO, JSONResponse]:
    try:
        return antibody_service.create_antibody(body, get_user_id())
    except AntibodyDataException as e:
        raise HTTPException(status_code=400, detail=dict(
            name=e.field_name, value=e.field_value))
    except antibody_service.DuplicatedAntibody as e:
        return JSONResponse(status_code=409, content=jsonable_encoder(e.antibody))
    except Exception as e:
        log.error("Error creating antibody: %s", e, exc_info=True)
        from pprint import pprint
        pprint(body.dict())
        raise e


def get_antibody(antibody_id: int) -> List[AntibodyDTO]:
    return antibody_service.get_antibody(antibody_id)


def update_user_antibody(accession_number: str, body: UpdateAntibodyDTO) -> AntibodyDTO:
    try:
        return antibody_service.update_antibody(get_user_id(), accession_number, body)
    except AntibodyDataException as e:
        raise HTTPException(status_code=400, detail=dict(
            name=e.field_name, value=e.field_value))


def delete_antibody(antibody_id: str) -> None:
    # FIXME this must be protected
    return antibody_service.delete_antibody(antibody_id)


def get_by_accession(accession_number: int) -> AntibodyDTO:
    try:
        return antibody_service.get_antibody_by_accession(accession_number)
    except Antibody.DoesNotExist as e:
        raise HTTPException(status_code=404, detail="Antibody not found")


def get_antibodies_export():
    from api.services.export_service import generate_antibodies_csv_file
    fname = "static/www/antibodies_export.csv"

    # check if file exists and it is created within 24 hours
    # if not, generate a new file
    if filesystem_service.check_if_file_does_not_exist_and_recent(fname):
        generate_antibodies_csv_file(fname)
    return RedirectResponse("/" + fname)
    # return FileResponse(fname, filename="antibodies_export.csv")


def get_antibodies_export_admin(status: Optional[AntibodyStatusEnum] = None):
    """
    Export all fields of all antibodies to a CSV file - Only for admin users
    """
    exception_msg = "Unauthorized: Only admin users can access this endpoint"
    try:
        is_admin = check_if_user_is_admin()
        if not is_admin:
            raise Exception(exception_msg)
    except Exception as e:
        raise HTTPException(status_code=401, detail=exception_msg)
    
    if status and status.value not in STATUS.values:
        raise HTTPException(status_code=400, detail="Invalid status")
    
    from api.services.export_service import generate_antibodies_fields_by_status_to_csv
    fname = f"static/www/antibodies_admin_export_{status.value}.csv" if status is not None \
        else "static/www/antibodies_admin_export.csv"

    if filesystem_service.check_if_file_does_not_exist_and_recent(fname):
        generate_antibodies_fields_by_status_to_csv(fname, status.value if status else '')    
    return RedirectResponse("/" + fname)
