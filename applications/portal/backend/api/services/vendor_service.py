from typing import Tuple

from api.models import Vendor
from api.utilities.exceptions import RequiredParameterMissing


def get_or_create_vendor(**kwargs) -> Tuple:
    name = kwargs.get('name', None)
    if name is None:
        raise RequiredParameterMissing('name')

    new = False
    try:
        vendor = Vendor.objects.get(name=name)
    except Vendor.DoesNotExist:
        vendor = Vendor(**kwargs)
        vendor.save()
        new = True
    return vendor, new
