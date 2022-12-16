from typing import Tuple

from api.models import Specie
from api.utilities.exceptions import RequiredParameterMissing


def get_or_create_specie(**kwargs) -> Tuple:
    name = kwargs.get('name', None)
    if name is None:
        raise RequiredParameterMissing('name')

    new = False
    try:
        specie = Specie.objects.get(name=name)
    except Specie.DoesNotExist:
        specie = Specie(**kwargs)
        specie.save()
        new = True
    return specie, new
