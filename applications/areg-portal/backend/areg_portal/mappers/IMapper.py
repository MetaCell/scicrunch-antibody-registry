from abc import ABC, abstractmethod


class IDAOMapper(ABC):

    @abstractmethod
    def to_dto(self, dao):
        pass

    @abstractmethod
    def from_dto(self, dto):
        pass
