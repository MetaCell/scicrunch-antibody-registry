"""
Django Ninja schemas for the Antibody Registry API
Based on the OpenAPI specification
Uses snake_case internally, camelCase in API via alias_generator
"""
from datetime import datetime, date
from typing import List, Optional, Union
from enum import Enum
from ninja import Schema
from pydantic import Field, field_serializer, ConfigDict


def to_camel(string: str) -> str:
    """Convert snake_case to camelCase"""
    components = string.split('_')
    return components[0] + ''.join(word.capitalize() for word in components[1:])


class CamelModelSchema(Schema):
    """Base schema class that converts snake_case field names to camelCase in API responses"""
    
    class Config(Schema.Config):
        alias_generator = to_camel
        populate_by_name = True  # Allow both snake_case and camelCase


class ValidationErrorDetail(Schema):
    type: str
    loc: list[Union[str, int]]
    msg: str
    ctx: dict | None = None
    
class ErrorResponseSchema(Schema):
    detail: Union[str, List[ValidationErrorDetail]] = None

# Enums
class ClonalityEnum(str, Enum):
    unknown = "unknown"
    cocktail = "cocktail"
    control = "control"
    isotype_control = "isotype control"
    monoclonal = "monoclonal"
    monoclonal_secondary = "monoclonal secondary"
    polyclonal = "polyclonal"
    polyclonal_secondary = "polyclonal secondary"
    oligoclonal = "oligoclonal"
    recombinant = "recombinant"
    recombinant_monoclonal = "recombinant monoclonal"
    recombinant_monoclonal_secondary = "recombinant monoclonal secondary"
    recombinant_polyclonal = "recombinant polyclonal"
    recombinant_polyclonal_secondary = "recombinant polyclonal secondary"


class CommercialTypeEnum(str, Enum):
    commercial = "commercial"
    non_profit = "non-profit"
    personal = "personal"
    other = "other"


class AntibodyStatusEnum(str, Enum):
    CURATED = "CURATED"
    REJECTED = "REJECTED"
    QUEUE = "QUEUE"
    UNDER_REVIEW = "UNDER_REVIEW"


class SortOrderEnum(str, Enum):
    asc = "asc"
    desc = "desc"


class OperationEnum(str, Enum):
    and_ = "and"
    or_ = "or"


# Utility schemas
class KeyValuePair(Schema):
    """Utility type to represent a key-value object"""
    key: str
    value: str


class KeyValueArrayPair(Schema):
    """Utility type to represent a key-value object where value is an array"""
    key: str
    value: List[str]


class KeyValueSortOrderPair(Schema):
    """Utility type to represent a key-value object with sort order"""
    key: str
    sortorder: SortOrderEnum


# Abstract/Base schemas
class AbstractAntibody(CamelModelSchema):
    """The common fields between all REST operations for the antibody resource"""
    clonality: Optional[ClonalityEnum] = None
    epitope: Optional[str] = None
    comments: Optional[str] = None
    url: Optional[str] = None
    ab_name: Optional[str] = Field(None)
    ab_target: Optional[str] = Field(None)
    clone_id: Optional[str] = Field(None)
    commercial_type: Optional[CommercialTypeEnum] = Field(None)
    defining_citation: Optional[str] = Field(None)
    product_conjugate: Optional[str] = Field(None)
    product_form: Optional[str] = Field(None)
    product_isotype: Optional[str] = Field(None)
    source_organism: Optional[str] = Field(None)
    target_species: Optional[List[str]] = Field(None)
    uniprot_id: Optional[str] = Field(None)
    applications: Optional[List[str]] = None
    kit_contents: Optional[str] = Field(None)
    ab_target_entrez_id: Optional[str] = Field(None)
    ab_target_uniprot_id: Optional[str] = Field(None)
    num_of_citation: Optional[int] = Field(None)


class AntibodyCoreId(CamelModelSchema):
    """Related attributes used to uniquely identify antibodies"""
    catalog_num: Optional[str] = Field(None)
    vendor_name: Optional[str] = Field(None)


# Request schemas
class AddAntibody(AbstractAntibody, AntibodyCoreId):
    """The data type associated with the POST method of the antibody resource"""
    url: str  # Required for AddAntibody


class UpdateAntibody(AbstractAntibody):
    """The data type associated with the PUT method of the antibody resource"""
    url: str  # Required for UpdateAntibody


# Response schemas
class Antibody(AbstractAntibody, AntibodyCoreId):
    """The data type associated with the antibody resource"""
    accession: Optional[int] = None
    status: Optional[AntibodyStatusEnum] = None
    feedback: Optional[str] = None
    ab_id: Optional[int] = None
    cat_alt: Optional[str] = None
    curate_time: Optional[datetime] = None
    curator_comment: Optional[str] = None
    disc_date: Optional[str] = None
    insert_time: Optional[datetime] = None
    target_modification: Optional[str] = None
    target_subregion: Optional[str] = None
    vendor_id: Optional[int] = None
    last_edit_time: Optional[datetime] = None
    ix: Optional[int] = None
    show_link: Optional[bool] = None
    vendor_url: Optional[List[str]] = None
    
    @staticmethod
    def resolve_source_organism(obj):
        """Convert source_organism Specie model to string"""
        if obj.source_organism:
            return obj.source_organism.name
        return None

    @staticmethod
    def resolve_target_species(obj):
        """Convert target_species Specie models to list of strings"""
        if obj.species:
            return [s.name for s in obj.species.all()]
        return None
    
    @staticmethod
    def resolve_applications(obj):
        """Convert applications to list of strings"""
        if obj.applications:
            return [a.name for a in obj.applications.all()]
        return None
    
    @staticmethod
    def resolve_vendor_name(obj):
        """Convert vendor to vendor name string"""
        if obj.vendor:
            return obj.vendor.name
        return None

    @staticmethod
    def resolve_vendor_url(obj):
        """Get vendor URLs from vendor domains"""
        if obj.vendor:
            from api.models import VendorDomain, STATUS
            domains = VendorDomain.objects.filter(vendor_id=obj.vendor.id, status=STATUS.CURATED)
            return [vd.base_url for vd in domains]
        return None

    @staticmethod
    def resolve_ab_target_entrez_id(obj):
        """Map entrez_id to ab_target_entrez_id"""
        return obj.entrez_id

    @staticmethod
    def resolve_ab_target_uniprot_id(obj):
        """Map uniprot_id to ab_target_uniprot_id"""
        return obj.uniprot_id

    @staticmethod
    def resolve_num_of_citation(obj):
        """Map citation to num_of_citation"""
        return obj.citation

    @staticmethod
    def resolve_url(obj):
        """Handle URL with permission checking"""
        from api.mappers.mapping_utils import get_url_if_permitted
        return get_url_if_permitted(obj)

    @staticmethod
    def resolve_show_link(obj):
        """Handle show_link logic"""
        return obj.show_link if obj.show_link is not None else (obj.vendor and obj.vendor.show_link)

    @staticmethod
    def resolve_catalog_num(obj):
        """Handle catalog_num with cat_alt appending"""
        if obj.cat_alt:
            catalog_num = obj.catalog_num or ""
            return f"{catalog_num} (also {obj.cat_alt})"
        return obj.catalog_num

    class Config(CamelModelSchema.Config):
        from_attributes = True  # Enable ORM mode for Django models


class PaginatedAntibodies(CamelModelSchema):
    """Paginated response for antibodies"""
    page: int
    total_elements: int
    items: List[Antibody]


# Other schemas
class DataInfo(Schema):
    """Information about the data in the system"""
    total: int
    lastupdate: date


class IngestRequest(CamelModelSchema):
    """Request body for data ingestion"""
    drive_link_or_id: Optional[str] = None
    hot: Optional[bool] = False


class FilterRequest(CamelModelSchema):
    """The search request body that allows filtering combinations over multiple columns"""
    contains: Optional[List[KeyValuePair]] = None
    equals: Optional[List[KeyValuePair]] = None
    page: Optional[int] = 1
    size: Optional[int] = 10
    search: Optional[str] = None
    ends_with: Optional[List[KeyValuePair]] = None
    sort_on: Optional[List[KeyValueSortOrderPair]] = None
    starts_with: Optional[List[KeyValuePair]] = None
    is_empty: Optional[List[str]] = None
    is_not_empty: Optional[List[str]] = None
    is_any_of: Optional[List[KeyValueArrayPair]] = None
    operation: Optional[OperationEnum] = None
    is_user_scope: Optional[bool] = None


class PartnerResponseObject(Schema):
    """Response of the list of partners and related images"""
    name: Optional[str] = None
    url: Optional[str] = None
    image: Optional[str] = None


class VendorSchema(Schema):
    """Vendor information"""
    id: Optional[int] = None
    name: Optional[str] = None
    url: Optional[str] = None
    description: Optional[str] = None


class TaskIdResponse(CamelModelSchema):
    """Response containing task ID for async operations"""
    task_id: str


class ExportRequest(Schema):
    """Request for exporting antibodies"""
    quick: Optional[bool] = False


class CitationJournalResult(CamelModelSchema):
    """Result from citation journal search"""
    pmid: Optional[str] = None
    article_title: Optional[str] = None
    journal: Optional[str] = None
    year: Optional[str] = None
    month: Optional[str] = None
    day: Optional[str] = None
    volume: Optional[str] = None
    pages: Optional[str] = None


class CitationJournalSearchResults(Schema):
    """Search results for citation journals"""
    results: List[CitationJournalResult]
