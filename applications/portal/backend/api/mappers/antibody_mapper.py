import datetime
import enum
from urllib.parse import urlsplit

from django.db import models
from pydantic import ValidationError

from api.mappers.imapper import IDAOMapper
from api.models import STATUS, Antibody, Antigen, Vendor, VendorDomain
from api.utilities.exceptions import AntibodyDataException
from cloudharness import log
from openapi.models import Antibody as AntibodyDTO
from .mapping_utils import dict_to_snake, dict_to_camel, to_snake
from ..services.gene_service import get_or_create_gene
from ..services.specie_service import get_or_create_specie

dto_fields = {to_snake(f) for f in AntibodyDTO.__fields__}


def extract_base_url(url):
    return urlsplit(url).hostname


class AntibodyMapper(IDAOMapper):

    def from_dto(self, dto: AntibodyDTO) -> Antibody:

        if hasattr(dto, "abId") and dto.abId:
            ab: Antibody = Antibody.objects.get(dto.abId)
        else:
            ab = Antibody()

        if dto.abTarget:
            antigen_symbol = dto.abTarget
            # del dto.abTarget
            gene, new = get_or_create_gene(symbol=antigen_symbol)
            ab.antigen = gene
            if new:
                # TODO what to do for non existing antigens? Create one? Should fill the table of antigens from a real data source?
                log.warn("No antigen: %s", antigen_symbol)

        if dto.sourceOrganism:
            specie_name = dto.sourceOrganism
            # del dto.sourceOrganism
            specie, new = get_or_create_specie(name=specie_name)
            ab.source_organism = specie
            if new:
                log.info("Adding specie: %s", specie_name)

        if dto.url:
            ab.vendor = self.vendor_from_antibody(dto)
        else:
            raise AntibodyDataException("Vendor url is mandatory", 'url', None)

        ab_dict = dict_to_snake(dto.dict())

        for k, v in ab_dict.items():
            if not v:
                continue
            if isinstance(v, enum.Enum):
                setattr(ab, k, v.value)
            elif not isinstance(v, (list, tuple)) and not getattr(ab, k, None):
                setattr(ab, k, v)
        ab.ab_id = 0
        ab.save()  # Need to save first to set the manytomany

        if dto.targetSpecies:
            species = []
            for specie_name in dto.targetSpecies:
                specie, new = get_or_create_specie(name=specie_name)
                species.append(specie)
                if new:
                    log.info("Adding specie: %s", specie_name)
            ab.species.set(species)

        return ab

    @staticmethod
    def vendor_from_antibody(dto: AntibodyDTO):
        # Vendor url check workflows https://github.com/MetaCell/scicrunch-antibody-registry/issues/51

        base_url = extract_base_url(dto.url)
        if not base_url:
            raise AntibodyDataException("Not a valid url", "url", dto.url)
        try:
            return VendorDomain.objects.get(base_url=base_url).vendor
        except VendorDomain.DoesNotExist:
            vendor_name = dto.vendorName or base_url
            log.info("Creating new Vendor `%s` on domain  to `%s`",
                     vendor_name, base_url)

            v = Vendor(name=vendor_name,
                       commercial_type=dto.commercialType.value)
            v.save()
            vd = VendorDomain(vendor=v, base_url=base_url, status=STATUS.QUEUE)
            vd.save()
            return v

    def to_dto(self, dao: Antibody) -> AntibodyDTO:
        dao_dict = dao.__dict__

        for k, v in dao_dict.items():
            if k == "_state":
                continue
            if isinstance(v, models.TextChoices):
                dao_dict[k] = v.value
            elif isinstance(v, datetime.date):
                dao_dict[k] = v.isoformat()
        try:
            ab = AntibodyDTO(**dict_to_camel(dao_dict), )
        except ValidationError as e:
            log.error("Validation error on antibody %s",
                      dao.ab_id, exc_info=True)
            from pprint import pprint
            pprint(dict_to_camel(dao_dict))
            ab = AntibodyDTO()
        if dao.antigen:
            antigen: Antigen = dao.antigen
            ab.abTarget = antigen.symbol
        if dao.vendor:
            ab.vendorName = dao.vendor.name
        if dao.source_organism:
            ab.sourceOrganism = dao.source_organism.name
        if dao.species and not ab.targetSpecies:
            ab.targetSpecies = [s.name for s in dao.species.all()]

        # ab.commercialType = dao.
        return ab
