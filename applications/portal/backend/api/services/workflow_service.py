import uuid

from cloudharness.workflows import operations
from cloudharness import log
from urllib.parse import urlparse
from urllib.parse import parse_qs

INGEST_OP = "areg-ingest-task-op"
INGEST_IMAGE = "portal"


def _create_task(image_name, **kwargs):
    from cloudharness.workflows import tasks

    return tasks.CustomTask(
        name=f"{image_name}-{str(uuid.uuid4())[:8]}", image_name=image_name, **kwargs,
        resources={"requests": {"cpu": "100m", "memory": "3Gi"}}
    )


def execute_ingestion_workflow(file_id: str, hot: bool = False):
    if hot:
        from django.db import transaction, connection

        from api.management.ingestion.ingestor import Ingestor
        from api.management.ingestion.preprocessor import Preprocessor
        log.info("Preprocessing started")
        metadata = Preprocessor(file_id).preprocess()
        log.info("Ingestion process started")
        with transaction.atomic():
            Ingestor(metadata, connection, hot).ingest()
        return
    ttl_strategy = {
        'secondsAfterCompletion': 60 * 60 * 24,
        'secondsAfterSuccess': 60 * 20,
        'secondsAfterFailure': 60 * 60 * 24
    }

    operations.PipelineOperation(
        basename=INGEST_OP,
        tasks=(
            _create_task(
                INGEST_IMAGE,
                command=["python", "manage.py", "ingest", file_id] + (["--hot"] if hot else [])
            ),
        ),
        ttl_strategy=ttl_strategy
    ).execute()
