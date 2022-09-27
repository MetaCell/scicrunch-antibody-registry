from email.mime import base
import enum
import datetime
from urllib.parse import urlsplit

from django.forms.models import model_to_dict
from django.db import models

from cloudharness import log
from api.models import STATUS, Antibody, AntibodyClonality, Gene, CommercialType, Specie, Vendor, VendorDomain, VendorSynonym
from openapi.models import Antibody as AntibodyDTO

from openapi import models as api_models
from api.mappers.imapper import IDAOMapper
from .mapping_utils import dict_to_snake, dict_to_camel, to_camel, to_snake

dto_fields = {to_snake(f) for f in AntibodyDTO.__fields__}

class AntibodyDataException(Exception): 
    def __init__(self, message, field_name, field_value):
        super().__init__(message)
        self.field_name = field_name
        self.field_value = field_value
class AntibodyMapper(IDAOMapper):

    def from_dto(self, dto: AntibodyDTO) -> Antibody:

        if hasattr(dto, "abId") and dto.abId:
            ab: Antibody = Antibody.objects.get(dto.abId)
        else:
            ab = Antibody()

        if dto.abTarget:
            antigen_symbol = dto.abTarget
            del dto.abTarget
            try:
                ab.antigen = Gene.objects.get(symbol=antigen_symbol)
            except Gene.DoesNotExist:
                # TODO what to do for non existing antigens? Create one? Should fill the table of antigens from a real data source?
                log.warn("No antigen: %s", antigen_symbol)
                ag = Gene(symbol=antigen_symbol)
                ag.save()
                ab.antigen = ag

        if dto.sourceOrganism:
            specie = dto.sourceOrganism
            del dto.sourceOrganism
            try:
                ab.source_organism = Specie.objects.get(name=specie)
            except Specie.DoesNotExist:
                log.info("Adding specie: %s", antigen_symbol)
                sp = Specie(name=specie)
                sp.save()
                ab.source_organism = sp
        if dto.url:
            # Vendor url check workflows https://github.com/MetaCell/scicrunch-antibody-registry/issues/51

            base_url = urlsplit(dto.url).hostname
            if not base_url:
                raise AntibodyDataException("Not a valid url", "url", dto.url)
            try:
                ab.vendor = VendorDomain.objects.get(base_url=base_url).vendor
            except VendorDomain.DoesNotExist:
                if dto.vendorName:
                    try:
                        v: Vendor = Vendor.objects.get(name=dto.vendorName)
                        
                        log.info("Adding new domain `%s` to vendor `%s`", base_url, v.name)
                        vd = VendorDomain(vendor=v, base_url=base_url, status=STATUS.QUEUE)
                        vd.save()
                        ab.vendor = v
                    except Vendor.DoesNotExist:
                        ab.vendor = self.vendor_from_name(dto)
        elif dto.vendorName:
            ab.vendor = self.vendor_from_name(dto)

        ab_dict = dict_to_snake(dto.dict())

        for k, v in ab_dict.items():
            if not v:
                continue
            if isinstance(v, enum.Enum):
                setattr(ab, k, v.value)
            else:
                setattr(ab, k, v)
        ab.ab_id = 0
        ab.save()  # Need to save first to set the manytomany

        if dto.targetSpecies:
            species = []
            for specie in dto.targetSpecies:
                try:
                    species.append(Specie.objects.get(name=specie))
                except Specie.DoesNotExist:
                    # TODO what to do for non existing antigens? Create one? Should fill the table of antigens from a real data source?
                    log.warn("Adding specie: %s", specie)
                    sp = Specie(name=specie)
                    sp.save()
                    species.append(sp)
            ab.species.set(species)

        return ab

    @staticmethod
    def vendor_from_name(dto):

        vendor_name = dto.vendorName
        del dto.vendorName
        try:
            return Vendor.objects.get(name=vendor_name)
        except Vendor.DoesNotExist:
            try:
                vendor_synonym: VendorSynonym = VendorSynonym.objects.get(
                    name=vendor_name)
                return vendor_synonym.vendor
            except VendorSynonym.DoesNotExist:
                log.warn("Adding vendor: %s", vendor_name)
                v = Vendor(name=vendor_name, )
                v.save()
                return v

    def to_dto(self, dao: Antibody) -> AntibodyDTO:
        # todo: implement @afonsobspinto

        dao_dict = dao.__dict__

         

        for k, v in dao_dict.items():
            if k == "_state":
                continue
            if isinstance(v, models.TextChoices):
                dao_dict[k] =  v.value
            elif isinstance(v, datetime.date):
                dao_dict[k] = v.isoformat()

        ab = AntibodyDTO(**dict_to_camel(dao_dict), )
        if dao.antigen:
            antigen: Gene = dao.antigen
            ab.abTarget = antigen.symbol
        if dao.vendor:
            ab.vendorName = dao.vendor.name
        # ab.commercialType = dao.
        return ab
