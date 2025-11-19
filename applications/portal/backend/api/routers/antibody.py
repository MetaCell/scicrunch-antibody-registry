"""
Antibody Router - Handles all antibody-related endpoints
"""
from datetime import datetime
from typing import List, Optional

from ninja import Router
from ninja.errors import HttpError
from django.http import HttpRequest
from django.shortcuts import redirect
from django.core.paginator import Paginator
from django.conf import settings
from django.db.models import Q
from cloudharness import log

from api.schemas import (
    AddAntibody,
    Antibody as AntibodySchema,
    AntibodyStatusEnum,
    PaginatedAntibodies,
    UpdateAntibody,
)
from api.helpers import CamelCaseRouter
from api.models import Antibody, STATUS
from api.services.user_service import check_if_user_is_admin
from api.services.specie_service import get_or_create_specie
from api.services.application_service import get_or_create_application
from api.services.export_service import generate_antibodies_csv_file
from api.utilities.exceptions import AntibodyDataException, DuplicatedAntibody
from api.utilities.functions import check_if_status_exists_or_curated


router = CamelCaseRouter()

# Import auth from api module
from api.api import auth


@router.get("/antibodies", response=PaginatedAntibodies, tags=["antibody"])
def get_antibodies(
    request: HttpRequest,
    page: Optional[int] = None,
    size: Optional[int] = None,
    updated_from: Optional[datetime] = None,
    updated_to: Optional[datetime] = None,
    status: Optional[str] = None,
):
    """List Antibodies"""
    if page is None:
        page = 1
    if size is None:
        size = 50
    if page < 1:
        raise HttpError(400, "Pages start at 1")
    if size < 1:
        raise HttpError(400, "Size must be greater than 0")
    if page * size > 500:
        if request.user.is_anonymous:
            raise HttpError(401, "Request not allowed")
    
    try:
        query = Antibody.objects.filter(status=check_if_status_exists_or_curated(status))
        if updated_from:
            query = query.filter(lastedit_time__gte=updated_from)
        if updated_to:
            query = query.filter(lastedit_time__lte=updated_to)

        p = Paginator(
            query.select_related("vendor", "source_organism")
            .prefetch_related("species", "applications")
            .order_by("-ix"),
            size
        )
        items = list(p.get_page(page))
        return {"page": int(page), "total_elements": p.count, "items": items}
    except Antibody.DoesNotExist:
        return {"page": int(page), "total_elements": 0, "items": []}
    except ValueError:
        raise HttpError(400, "Page and size must be integers")


@router.post("/antibodies", response={201: AntibodySchema}, tags=["antibody"], auth=auth)
def create_antibody(request: HttpRequest, body: AddAntibody):
    """Create a Antibody"""
    if request.user.is_anonymous:
        raise HttpError(401, "Unrecognized user")
    
    user_id = request.user.member.kc_id
    
    try:
        antibody = Antibody()
        antibody.ab_id = 0
        
        if body.ab_target:
            antibody.ab_target = body.ab_target
        
        if body.source_organism:
            specie, new = get_or_create_specie(name=body.source_organism)
            antibody.source_organism = specie
            if new:
                log.info("Adding specie: %s", body.source_organism)
        
        if body.url or body.vendor_name:
            antibody.set_vendor_from_name_url(
                url=body.url,
                name=body.vendor_name,
                commercial_type=body.commercial_type.value if body.commercial_type else None
            )
        else:
            raise AntibodyDataException("Either vendor url or name is mandatory", 'url/name', None)
        
        # Map all the fields from schema to model
        for field in ['clonality', 'epitope', 'comments', 'url', 'clone_id', 
                      'defining_citation', 'product_conjugate', 'product_form', 
                      'product_isotype', 'uniprot_id', 'kit_contents', 'catalog_num']:
            value = getattr(body, field, None)
            if value is not None:
                if hasattr(value, 'value'):  # Enum
                    setattr(antibody, field, value.value)
                elif isinstance(value, str):
                    setattr(antibody, field, value.strip())
                else:
                    setattr(antibody, field, value)
        
        if body.ab_name:
            antibody.ab_name = body.ab_name.strip()
        if body.commercial_type:
            antibody.commercial_type = body.commercial_type.value
        if body.ab_target_entrez_id:
            antibody.entrez_id = body.ab_target_entrez_id
        if body.ab_target_uniprot_id:
            antibody.uniprot_id = body.ab_target_uniprot_id
        if body.target_species:
            antibody.target_species_raw = ','.join(body.target_species)
        
        antibody.uid = user_id
        antibody.save()
        
        # Handle applications many-to-many relation
        if body.applications:
            for app_name in body.applications:
                if app_name:  # Skip empty strings
                    application, created = get_or_create_application(app_name)
                    antibody.applications.add(application)

        if antibody.accession != antibody.ab_id:
            # Raise DuplicatedAntibody exception which will be handled by the exception handler
            raise DuplicatedAntibody(antibody)

        return 201, antibody
    except AntibodyDataException as e:
        raise HttpError(400, {"name": e.field_name, "value": e.field_value})
    except Exception as e:
        log.error("Error creating antibody: %s", e, exc_info=True)
        raise e


@router.get("/antibodies/export", tags=["antibody"], auth=auth)
def get_antibodies_export(request: HttpRequest):
    """Export all antibodies in csv format"""
    from api.services.filesystem_service import check_if_file_does_not_exist_and_recent
    
    fname = "static/www/antibodies_export.csv"
    if check_if_file_does_not_exist_and_recent(fname):
        generate_antibodies_csv_file(fname)
    return redirect("/" + fname)


@router.get("/antibodies/export/admin", tags=["antibody"], auth=auth)
def get_antibodies_export_admin(
    request: HttpRequest, status: Optional[AntibodyStatusEnum] = None
):
    """Export all fields of all antibodies to a CSV file - Only for admin users"""
    try:
        is_admin = check_if_user_is_admin()
        if not is_admin:
            raise HttpError(401, "Unauthorized: Only admin users can access this endpoint")
    except Exception:
        raise HttpError(401, "Unauthorized: Only admin users can access this endpoint")
    
    if status and status.value not in STATUS.values:
        raise HttpError(400, "Invalid status")
    
    from api.services.export_service import generate_antibodies_fields_by_status_to_csv
    from api.services.filesystem_service import check_if_file_does_not_exist_and_recent
    
    fname = f"static/www/antibodies_admin_export_{status.value}.csv" if status is not None \
        else "static/www/antibodies_admin_export.csv"

    if check_if_file_does_not_exist_and_recent(fname):
        generate_antibodies_fields_by_status_to_csv(fname, status.value if status else '')    
    return redirect("/" + fname)


@router.get("/antibodies/user", response=PaginatedAntibodies, tags=["antibody"], auth=auth)
def get_user_antibodies(
    request: HttpRequest, page: Optional[int] = None, size: Optional[int] = None
):
    """List user's Antibodies"""
    if page is None:
        page = 1
    if size is None:
        size = 50
    if page < 1:
        raise HttpError(400, "Pages start at 1")
    if size < 1:
        raise HttpError(400, "Size must be greater than 0")
    if size > 100:
        raise HttpError(400, "Size must be less than 100")
    
    if request.user.is_anonymous:
        raise HttpError(401, "Unrecognized user")
    
    user_id = request.user.member.kc_id
    p = Paginator(Antibody.objects.filter(uid=user_id).order_by("-ix"), size)
    items = list(p.get_page(page))
    return {"page": int(page), "total_elements": p.count, "items": items}


@router.get("/antibodies/user/{accession_number}", response=AntibodySchema, tags=["antibody"])
def get_by_accession(request: HttpRequest, accession_number: int):
    """Get antibody by the accession number"""
    try:
        antibody = Antibody.objects.select_related("vendor", "source_organism") \
            .prefetch_related("species", "applications") \
            .get(accession=accession_number)
        return antibody
    except Antibody.DoesNotExist:
        raise HttpError(404, "Antibody not found")
    except Antibody.MultipleObjectsReturned:
        log.warning(f"Multiple antibodies with accession {accession_number}")
        raise HttpError(500, "Multiple antibodies found")


@router.put("/antibodies/user/{accession_number}", response={202: AntibodySchema}, tags=["antibody"], auth=auth)
def update_user_antibody(
    request: HttpRequest, accession_number: int, body: UpdateAntibody
):
    """Update a submitted Antibody"""
    if request.user.is_anonymous:
        raise HttpError(401, "Unrecognized user")
    
    user_id = request.user.member.kc_id
    
    try:
        current_antibody = Antibody.objects.get(accession=accession_number, uid=user_id)
        
        # Update fields from body
        if body.ab_target:
            current_antibody.ab_target = body.ab_target
        if body.source_organism:
            specie, new = get_or_create_specie(name=body.source_organism)
            current_antibody.source_organism = specie
        
        # Map all the fields
        for field in ['clonality', 'epitope', 'comments', 'url', 'clone_id', 
                      'defining_citation', 'product_conjugate', 'product_form', 
                      'product_isotype', 'uniprot_id', 'kit_contents']:
            value = getattr(body, field, None)
            if value is not None:
                if hasattr(value, 'value'):  # Enum
                    setattr(current_antibody, field, value.value)
                elif isinstance(value, str):
                    setattr(current_antibody, field, value.strip())
                else:
                    setattr(current_antibody, field, value)
        
        if body.ab_name:
            current_antibody.ab_name = body.ab_name.strip()
        if body.commercial_type:
            current_antibody.commercial_type = body.commercial_type.value
        if body.ab_target_entrez_id:
            current_antibody.entrez_id = body.ab_target_entrez_id
        if body.ab_target_uniprot_id:
            current_antibody.uniprot_id = body.ab_target_uniprot_id
        if body.target_species:
            current_antibody.target_species_raw = ','.join(body.target_species)
        
        current_antibody.status = STATUS.QUEUE
        current_antibody.save()
        
        # Handle applications many-to-many relation
        if body.applications is not None:  # Check for None to allow clearing applications
            # Clear existing applications
            current_antibody.applications.clear()
            # Add new applications
            for app_name in body.applications:
                if app_name:  # Skip empty strings
                    application, created = get_or_create_application(app_name)
                    current_antibody.applications.add(application)
        
        return 202, current_antibody
    except AntibodyDataException as e:
        raise HttpError(400, {"name": e.field_name, "value": e.field_value})
    except Antibody.DoesNotExist:
        raise HttpError(404, "Antibody not found")


@router.get("/antibodies/{antibody_id}", response=List[AntibodySchema], tags=["antibody"])
def get_antibody(request: HttpRequest, antibody_id: int):
    """Get a Antibody"""
    user = request.user
    if user.is_anonymous:
        antibodies = Antibody.objects.filter(
            Q(ab_id=antibody_id) | Q(accession=antibody_id),
            status=STATUS.CURATED
        )
    else:
        antibodies = Antibody.objects.filter(
            Q(ab_id=antibody_id) | Q(accession=antibody_id)
        ).filter(
            Q(status=STATUS.CURATED) | Q(uid=user.member.kc_id)
        )
            
    return list(antibodies.select_related("vendor", "source_organism") \
            .prefetch_related("species", "applications"))

@router.post("/antibodies/export", response=str, tags=["antibody"], auth=auth)
def export_antibodies_post(request: HttpRequest):
    """Export antibodies as CSV"""
    if request.user.is_anonymous:
        raise HttpError(401, "Unrecognized user")
    
    # Generate CSV file
    import os
    import tempfile
    fname = os.path.join(tempfile.gettempdir(), "antibodies_export.csv")
    
    # Check if file exists and is recent (within 24 hours)
    from api.services import filesystem_service
    if filesystem_service.check_if_file_does_not_exist_and_recent(fname):
        generate_antibodies_csv_file(fname)
    
    # Read and return CSV content
    with open(fname, 'r') as f:
        return f.read()
