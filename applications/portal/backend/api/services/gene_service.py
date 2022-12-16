from typing import Tuple

from api.models import Gene


def get_or_create_gene(symbol: str, **kwargs) -> Tuple:
    new = False
    try:
        gene = Gene.objects.get(symbol=symbol)
    except Gene.DoesNotExist:
        gene = Gene(symbol=symbol, **kwargs)
        gene.save()
        new = True
    return gene, new
