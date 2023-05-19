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
from openapi.models import AbstractAntibody as AbstractAntibodyDTO
from .mapping_utils import dict_to_snake, dict_to_camel, to_snake
from ..services.gene_service import get_or_create_gene
from ..services.specie_service import get_or_create_specie

dto_fields = {to_snake(f) for f in AntibodyDTO.__fields__}


def extract_base_url(url):
    return urlsplit(url).hostname


class AntibodyMapper(IDAOMapper):

    def from_dto(self, dto: AbstractAntibodyDTO) -> Antibody:
        if hasattr(dto, "abId") and dto.abId:
            ab: Antibody = Antibody.objects.get(ab_id=dto.abId)
        else:
            ab = Antibody()
            ab.ab_id = 0

        if dto.abTarget:
            # antigen_symbol = dto.abTarget
            # del dto.abTarget
            # gene, new = get_or_create_gene(symbol=antigen_symbol)
            ab.ab_target = dto.abTarget

        if dto.sourceOrganism:
            specie_name = dto.sourceOrganism
            # del dto.sourceOrganism
            specie, new = get_or_create_specie(name=specie_name)
            ab.source_organism = specie
            if new:
                log.info("Adding specie: %s", specie_name)

        if dto.url or dto.vendorName:
            ab.set_vendor_from_name_url(url=dto.url, name=dto.vendorName)
        else:
            raise AntibodyDataException(
                "Either vendor url or name is mandatory", 'url/name', None)

        ab_dict = dict_to_snake(dto.dict())

        for k, v in ab_dict.items():
            if not v:
                continue
            if isinstance(v, enum.Enum):
                setattr(ab, k, v.value)
            elif not isinstance(v, (list, tuple)) and (getattr(ab, k, None) is None or isinstance(getattr(ab, k, None),
                                                                                                  (int, str))):
                setattr(ab, k, v)

        if dto.targetSpecies:
            # the logic to create species and fill the field is in the model save automations
            ab.target_species_raw = ','.join(dto.targetSpecies)

        ab.save()  # Need to save to set the manytomany

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
            ab_dict = dict_to_camel(dao_dict)
            ab = AntibodyDTO(**ab_dict, )
        except ValidationError as e:
            log.error("Validation errors on antibody %s",
                      dao.ab_id, exc_info=True)
            for error in e.raw_errors:
                for loc in error.loc_tuple():
                    del ab_dict[loc]
            try:
                ab = AntibodyDTO(**ab_dict, )
            except ValidationError as e:
                log.error("Unrecoverable validation errors on antibody %s",
                          dao.ab_id, exc_info=True)
                ab = AntibodyDTO(abId=dao.ab_id, abName=dao.ab_name)
        except Exception as e:
            log.error("Unrecoverable errors on antibody %s",
                      dao.ab_id, exc_info=True)
            ab = AntibodyDTO(abId=dao.ab_id, abName=dao.ab_name)
        if dao.ab_target:
            ab.abTarget = dao.ab_target
        if dao.vendor:
            ab.vendorName = dao.vendor.name
        if dao.source_organism:
            ab.sourceOrganism = dao.source_organism.name
        if dao.species and not ab.targetSpecies:
            ab.targetSpecies = [s.name for s in dao.species.all()]

        if not dao.show_link:
            if dao.show_link is not None or (dao.vendor and not dao.vendor.show_link):
                try:
                    ab.url = VendorDomain.objects.filter(
                        vendor=dao.vendor).first().base_url
                except (VendorDomain.DoesNotExist, AttributeError):
                    ab.url = None

        if ab.url and "//" not in ab.url:
            ab.url = "//" + ab.url

        if dao.cat_alt:
            ab.catalogNum = ab.catalogNum + " (also " + dao.cat_alt + ")"

        # ab.commercialType = dao.
        return ab
