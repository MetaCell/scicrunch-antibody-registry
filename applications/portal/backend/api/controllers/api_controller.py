from openapi.models import DataInfo, PartnerResponseObject
from api.services import antibody_service, partner_service
from typing import List
from django.conf import settings
from api.utilities.cache import ttl_cache


@ttl_cache(maxsize=128, ttl=3600)
def get_datainfo():
    return DataInfo(total=antibody_service.count(), lastupdate=antibody_service.last_update())

def get_partners() -> List[PartnerResponseObject]:
    return [
        PartnerResponseObject(
            name=partner.name,
            url=partner.url,
            image=f"{settings.MEDIA_URL}{partner.image}" if partner.image else None
        ) for partner in partner_service.get_all_partners()
    ]