from api.models import Antibody
from openapi.models import Antibody as AntibodyDTO
from api.mappers.IMapper import IDAOMapper


class AntibodyMapper(IDAOMapper):
    def from_dto(self, dto) -> Antibody:
        # todo: implement @afonsobspinto
        pass

    def to_dto(self, dao: Antibody) -> AntibodyDTO:
        # todo: implement @afonsobspinto
        pass
