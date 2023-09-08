from fastapi import status

from api.services.workflow_service import execute_ingestion_workflow
from openapi.models import IngestRequest

def ingest(body: IngestRequest):
    execute_ingestion_workflow(body.driveLinkOrId, body.hot)
    return status.HTTP_200_OK
