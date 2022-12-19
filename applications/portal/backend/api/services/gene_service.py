from typing import Tuple

from api.models import Gene
from api.utilities.exceptions import RequiredParameterMissing


def get_or_create_gene(**kwargs) -> Tuple:
    symbol = kwargs.get('symbol', None)
    if symbol is None:
        raise RequiredParameterMissing('symbol')

    new = False
    try:
        gene = Gene.objects.get(symbol=symbol)
    except Gene.DoesNotExist:
        gene = Gene(**kwargs)
        gene.save()
        new = True
    return gene, new
