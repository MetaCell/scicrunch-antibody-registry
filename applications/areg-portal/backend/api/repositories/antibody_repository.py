from typing import List

from api.models import Antibody


def get_all(page: int = 0, size: int = 50) -> List[Antibody]:
    offset = page * size
    limit = offset + size
    return Antibody.objects.all()[offset:limit]


def update_or_create(antibody: Antibody):
    antibody.save()


def get(antibody_id: str):
    return Antibody.objects.get(ab_id=antibody_id)


def delete(antibody_id: str):
    antibody = get(antibody_id)
    return antibody.delete()
