from api.models import Vendor


def create_vendor(name: str) -> Vendor:
    return Vendor.objects.create(name=name)
