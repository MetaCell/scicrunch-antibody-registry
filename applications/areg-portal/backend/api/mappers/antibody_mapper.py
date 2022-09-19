from django.forms.models import model_to_dict

from cloudharness import log
from api.models import Antibody, AntibodyClonality, Antigen, Specie, Vendor
from openapi.models import Antibody as AntibodyDTO
from api.mappers.imapper import IDAOMapper
from .mapping_utils import dict_to_snake, dict_to_camel, to_snake

dto_fields = {to_snake(f) for f in AntibodyDTO.__fields__}
class AntibodyMapper(IDAOMapper):

    def from_dto(self, dto: AntibodyDTO) -> Antibody:
        
        if hasattr(dto, "abId") and dto.abId:
            ab: Antibody = Antibody.objects.get(dto.abId)
        else:
            ab = Antibody()
            
        ab_dict = dict_to_snake(dto.dict())
        
            
        if dto.abTarget:
            antigen_symbol = dto.abTarget
            del dto.abTarget
            try:
                ab.antigen = Antigen.objects.get(symbol=antigen_symbol)
            except Antigen.DoesNotExist:
                # TODO what to do for non existing antigens? Create one? Should fill the table of antigens from a real data source?
                log.warn("No antigen: %s", antigen_symbol)
                ag = Antigen(symbol=antigen_symbol)
                ag.save()
                ab.antigen = ag
        if dto.vendorId:
            vendor_id = dto.vendorId
            del dto.vendorId
            try:
                ab.vendor = Vendor.objects.get(nif_id=vendor_id)
            except Vendor.DoesNotExist:
                # TODO what to do for non existing antigens? Create one? Should fill the table of antigens from a real data source?
                log.warn("No antigen: %s", antigen_symbol)

        

        ab.save() # Need to save first to set the manytomany

        if dto.targetSpecies:
            species = []
            for specie in dto.targetSpecies:
                try:
                    species.append(Specie.objects.get(name=specie))
                except Specie.DoesNotExist:
                    # TODO what to do for non existing antigens? Create one? Should fill the table of antigens from a real data source?
                    log.warn("Adding specie: %s", antigen_symbol)
                    sp = Specie(name=specie)
                    sp.save()
                    species.append(sp)
            ab.species.set(species)
        if dto.sourceOrganism:
            try:
                ab.source_organism = Specie.objects.get(name=specie)
            except Specie.DoesNotExist:
                    # TODO what to do for non existing antigens? Create one? Should fill the table of antigens from a real data source?
                    log.warn("Adding specie: %s", antigen_symbol)
                    sp = Specie(name=specie)
                    sp.save()
                    ab.source_organism = sp
        for k, v in ab_dict.items():
            setattr(ab, k, v)
        return ab

    def to_dto(self, dao: Antibody) -> AntibodyDTO:
        # todo: implement @afonsobspinto
        dao_dict = model_to_dict(dao, fields=dto_fields)
        dao_dict["clonality"] = str(dao.clonality)
        dao_dict["commercial_type"] = str(dao_dict["commercial_type"].value)
        ab = AntibodyDTO(**dict_to_camel(dao_dict))
        ab.abTarget = dao.antigen.symbol
        # ab.commercialType = dao.
        return ab
