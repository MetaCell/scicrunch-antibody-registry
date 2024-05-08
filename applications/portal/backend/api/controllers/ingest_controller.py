from fastapi import HTTPException, status

from api.services.workflow_service import execute_ingestion_workflow
from openapi.models import IngestRequest
from api.services.keycloak_service import KeycloakService
from api.models import Antibody, STATUS
from api.utilities.exceptions import AntibodyDoesNotExist


def ingest(body: IngestRequest):
    auth = KeycloakService()
    try:
        if not auth.current_user_has_realm_role("administrator"):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail="You are not authorized to ingest data.")
    except:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail="You are not authorized to ingest data.")
    execute_ingestion_workflow(body.driveLinkOrId, body.hot)
    return status.HTTP_200_OK


def ingest_scicrunch_citation_metric(antibody_id, number_of_citation):
    try:
        antibodies_filtered_by_id = Antibody.objects.filter(ab_id=antibody_id)
        if not antibodies_filtered_by_id:
            raise Antibody.DoesNotExist
        for antibody in antibodies_filtered_by_id:
            antibody.citation = number_of_citation
            antibody.save()
        return status.HTTP_200_OK
    except AntibodyDoesNotExist as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
