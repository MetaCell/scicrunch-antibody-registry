import uuid

from cloudharness.workflows import operations

INGEST_OP = "areg-ingest-task-op"
INGEST_IMAGE = "areg-portal"


def _create_task(image_name, **kwargs):
    from cloudharness.workflows import tasks

    return tasks.CustomTask(
        name=f"{image_name}-{str(uuid.uuid4())[:8]}", image_name=image_name, **kwargs
    )


def execute_ingestion_workflow(file_id: str):
    operations.PipelineOperation(
        basename=INGEST_OP,
        tasks=(
            _create_task(
                INGEST_IMAGE,
                command=["python", "manage.py", "ingest", file_id]
            ),
        ),
    ).execute()
