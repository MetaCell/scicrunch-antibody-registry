from typing import Tuple

from api.models import Antigen
from api.utilities.exceptions import RequiredParameterMissing


def get_or_create_gene(**kwargs) -> Tuple:
    symbol = kwargs.get('symbol', None)
    if symbol is None:
        raise RequiredParameterMissing('symbol')

    new = False
    try:
        gene = Antigen.objects.get(symbol=symbol)
    except Antigen.DoesNotExist:
        gene = Antigen(**kwargs)
        gene.save()
        new = True
    return gene, new
