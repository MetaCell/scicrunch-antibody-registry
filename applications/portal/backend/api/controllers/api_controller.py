from openapi.models import DataInfo
from api.services import antibody_service


def get_datainfo():
    return DataInfo(total=antibody_service.count(), lastupdate=antibody_service.last_update())
