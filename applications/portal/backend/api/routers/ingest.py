"""
Ingest Router - Handles data ingestion endpoints
"""
from ninja import Router
from ninja.errors import HttpError
from django.http import HttpRequest

from api.schemas import IngestRequest
from api.helpers import CamelCaseRouter
from api.services.keycloak_service import KeycloakService
from api.services.workflow_service import execute_ingestion_workflow


router = CamelCaseRouter()

# Import auth from api module
from api.api import auth


@router.post("/ingest", response={200: dict}, tags=["ingest"], auth=auth)
def ingest(request: HttpRequest, body: IngestRequest):
    """Ingest antibody's csv data into the database"""
    auth_service = KeycloakService()
    try:
        if not auth_service.current_user_has_realm_role("administrator"):
            raise HttpError(401, "You are not authorized to ingest data.")
    except:
        raise HttpError(401, "You are not authorized to ingest data.")
    
    execute_ingestion_workflow(body.driveLinkOrId, body.hot)
    return {"status": "ok"}
