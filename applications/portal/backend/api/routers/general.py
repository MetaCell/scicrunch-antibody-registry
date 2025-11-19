"""
General Router - Handles general API endpoints like datainfo and partners
"""
from typing import List

from ninja import Router
from django.http import HttpRequest
from django.conf import settings
from django.utils.timezone import now
import dateutil.relativedelta
from cloudharness import log

from api.schemas import DataInfo, PartnerResponseObject
from api.models import Antibody, AntibodyStats, STATUS
from api.services.partner_service import get_all_partners


router = Router()


@router.get("/datainfo", response=DataInfo, tags=["general"])
def get_datainfo(request: HttpRequest):
    """Get data information"""
    # Use cached statistics for fast count
    try:
        total = AntibodyStats.objects.filter(status=STATUS.CURATED).values_list('count', flat=True).first()
        if total is None:
            # Fallback if stats table is empty
            total = Antibody.objects.filter(status=STATUS.CURATED).count()
    except Exception as e:
        log.warning(f"Failed to get count from AntibodyStats, using direct count: {e}")
        total = Antibody.objects.filter(status=STATUS.CURATED).count()
    
    # Get last update date
    last_date = now() - dateutil.relativedelta.relativedelta(months=6)
    try:
        last_update = Antibody.objects.filter(status=STATUS.CURATED, curate_time__gte=last_date) \
            .latest("curate_time").curate_time.date()
    except Antibody.DoesNotExist:
        last_update = now().date()
    
    return DataInfo(total=total, lastupdate=last_update)


@router.get("/partners", response=List[PartnerResponseObject], tags=["general"])
def get_partners(request: HttpRequest):
    """Get the list of partners and related images"""
    partners = get_all_partners()
    return [
        PartnerResponseObject(
            name=partner.name,
            url=partner.url,
            image=f"{settings.MEDIA_URL}{partner.image}" if partner.image else None
        ) for partner in partners
    ]
