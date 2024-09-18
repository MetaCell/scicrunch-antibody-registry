import datetime
import enum
from functools import cache
from urllib.parse import urlsplit

from django.db import models
from pydantic import ValidationError

from api.mappers.imapper import IDAOMapper
from api.models import STATUS, Antibody, Antigen, Vendor, VendorDomain
from api.utilities.exceptions import AntibodyDataException
from cloudharness import log
from openapi.models import Antibody as AntibodyDTO
from openapi.models import AbstractAntibody as AbstractAntibodyDTO
from .mapping_utils import dict_to_snake, dict_to_camel, to_snake, get_url_if_permitted
from ..services.gene_service import get_or_create_gene
from ..services.specie_service import get_or_create_specie

dto_fields = {to_snake(f) for f in AntibodyDTO.__fields__}


def extract_base_url(url):
    return urlsplit(url).hostname


def get_vendor_domains(vendor_id):
    return [vd.base_url for vd in VendorDomain.objects.filter(vendor_id=vendor_id, status=STATUS.CURATED)]


class AntibodyMapper(IDAOMapper):

    def from_dto(self, dto: AntibodyDTO) -> Antibody:
        if hasattr(dto, "ix") and dto.ix:
            ab: Antibody = Antibody.objects.get(pk=dto.ix)
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
            ab.set_vendor_from_name_url(
                url=dto.url, name=dto.vendorName,
                commercial_type=dto.commercialType.value if dto.commercialType else None
            )
        else:
            raise AntibodyDataException(
                "Either vendor url or name is mandatory", 'url/name', None)

        ab_dict = dict_to_snake(dto.dict())

        for k, v in ab_dict.items():
            if not v:
                continue
            try:
                if isinstance(v, str):
                    v = v.strip()
                if isinstance(v, enum.Enum):
                    setattr(ab, k, v.value)
                elif not isinstance(v, (list, tuple))\
                    and (getattr(ab, k, None) is None or
                         isinstance(getattr(ab, k, None), (int, str))):
                    setattr(ab, k, v)
            except Exception as e:
                log.exception("Error setting attribute %s, value: %s", k, v)

        if dto.targetSpecies:
            # the logic to create species and fill the field is in the model save automations
            ab.target_species_raw = ','.join(dto.targetSpecies)

        ab.save()  # Need to save to set the manytomany

        return ab

    def to_dto(self, dao: Antibody) -> AntibodyDTO:
        dao_dict = dao.__dict__

        for k, v in dao_dict.items():
            if k == "_state":
                continue
            try:
                if isinstance(v, models.TextChoices):
                    dao_dict[k] = v.value
                elif isinstance(v, datetime.date):
                    dao_dict[k] = v
            except Exception as e:
                log.exception("Error on antibody %s marshaling. Cannot set attribute %s, value: %s", k, v)
        try:
            ab_dict = dict_to_camel(dao_dict)
            ab_dict['lastEditTime'] = dao_dict['lastedit_time']  # mandatory, the dao dict key is not a proper snake-case variable name
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
        if dao.applications:
            ab.applications = [a.name for a in dao.applications.all()]
        if dao.entrez_id:
            ab.abTargetEntrezId = dao.entrez_id
        if dao.uniprot_id:
            ab.abTargetUniprotId = dao.uniprot_id
        if dao.vendor:
            ab.vendorName = dao.vendor.name
            ab.vendorUrl = get_vendor_domains(dao.vendor.id)
        if dao.source_organism:
            ab.sourceOrganism = dao.source_organism.name
        if dao.species and not ab.targetSpecies:
            ab.targetSpecies = [s.name for s in dao.species.all()]

        ab.numOfCitation = dao.citation
        ab.url = get_url_if_permitted(dao)

        ab.showLink = dao.show_link if dao.show_link is not None else (dao.vendor and dao.vendor.show_link)

        if dao.cat_alt:
            ab.catalogNum = ab.catalogNum + " (also " + dao.cat_alt + ")"

        # ab.commercialType = dao.
        return ab
