from typing import Tuple

from api.models import Specie


def get_or_create_specie(name: str, **kwargs) -> Tuple:
    new = False
    try:
        specie = Specie.objects.get(name=name)
    except Specie.DoesNotExist:
        specie = Specie(name=name, **kwargs)
        specie.save()
        new = True
    return specie, new
