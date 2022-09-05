from typing import List

from openapi.models import AddUpdateAntibody, Antibody


def get_antibodies(page: int = 0, size: int = 50) -> List[Antibody]:
    return []


def create_antibody(body: AddUpdateAntibody) -> None:
    return


def get_antibody(antibody_id: str) -> Antibody:
    return


def update_antibody(antibody_id: str, body: AddUpdateAntibody) -> None:
    return


def delete_antibody(antibody_id: str) -> None:
    return
