from django.contrib import admin
from django.db.models import Q
from django.utils.html import format_html, format_html_join
from import_export.admin import ImportMixin

from api.forms.AntibodyImportForm import AntibodyImportForm
from api.models import (
    STATUS,
    Antibody,
    AntibodyApplications,
    AntibodySpecies,
    Application,
    Gene,
    Vendor,
    Specie,
    VendorDomain,
    VendorSynonym,
)
from api.resources.AntibodyResource import AntibodyResource
from portal.settings import FOR_NEW_KEY, FOR_EXTANT_KEY, METHOD_KEY


@admin.display(description="ab_id")
def id_with_ab(obj: Antibody):
    return f"AB_{obj.ab_id}"


class AntibodySpeciesInline(admin.TabularInline):
    model = AntibodySpecies
    extra = 0


class AntibodyApplicationsInline(admin.TabularInline):
    model = AntibodyApplications
    extra = 0


@admin.register(Antibody)
class AntibodyAdmin(ImportMixin, admin.ModelAdmin):
    import_template_name = 'admin/import_export/custom_import_form.html'
    import_form_class = AntibodyImportForm
    resource_classes = [AntibodyResource]
    list_filter = ("status",)
    list_display = (id_with_ab, "ab_name", "status")
    search_fields = ("ab_id", "ab_name", "catalog_num")
    # readonly_fields = ("ab_id", "catalog_num", "accession")
    autocomplete_fields = ("vendor", "antigen", "species", "source_organism")
    inlines = (AntibodySpeciesInline, AntibodyApplicationsInline)

    def get_resource_kwargs(self, request, *args, **kwargs):
        rk = super().get_resource_kwargs(request, *args, **kwargs)
        rk['request'] = request
        return rk

    def get_import_data_kwargs(self, request, *args, **kwargs):
        kwargs[FOR_NEW_KEY] = request.POST.get(FOR_NEW_KEY, None)
        kwargs[FOR_EXTANT_KEY] = request.POST.get(FOR_EXTANT_KEY, None)
        kwargs[METHOD_KEY] = request.POST.get(METHOD_KEY, None)
        return super().get_import_data_kwargs(request, *args, **kwargs)


    def get_search_results(self, request, queryset, search_term):
        queryset, may_have_duplicates = super().get_search_results(
            request,
            queryset,
            search_term,
        )
        search_term = search_term.strip()
        if search_term.lower().startswith("ab_"):
            queryset |= self.model.objects.filter(ab_id=search_term[3:])
        return queryset, may_have_duplicates


@admin.register(Gene)
class GeneAdmin(admin.ModelAdmin):
    search_fields = ("symbol", "entrez_id", "uniprot_id")


@admin.register(Specie)
class SpecieAdmin(admin.ModelAdmin):
    search_fields = ("name",)


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    search_fields = ("name",)


class NonCuratedDomains(admin.SimpleListFilter):
    title = "Vendor Domain Status"

    # Parameter for the filter that will be used in the URL query.
    parameter_name = "curated_domain"

    def lookups(self, request, model_admin):
        return (
            ("Non-curated", ("Vendors with non-curated domains")),
            ("Curated", ("Vendors with curated domains")),
        )

    def queryset(self, request, queryset):
        if self.value() == "Non-curated":
            return queryset.filter(~Q(vendordomain__status=STATUS.CURATED))
        if self.value() == "Curated":
            return queryset.filter(vendordomain__status=STATUS.CURATED)


class VendorSynonymInline(admin.TabularInline):
    model = VendorSynonym
    show_change_link = True
    extra = 0


class VendorDomainInline(admin.TabularInline):
    model = VendorDomain
    fields = ("base_url", "status")
    # readonly_fields = ("base_url", "status")
    show_change_link = True
    extra = 0


# @admin.register(VendorDomain)
# class VendorDomainAdmin(admin.ModelAdmin):
#     list_display = (
#         "base_url",
#         "vendor",
#         "status",
#         "is_domain_visible",
#     )
#     list_editable = ("is_domain_visible",)


@admin.register(Vendor)
class VendorAdmin(admin.ModelAdmin):
    delete_confirmation_template = "admin/vendor/delete_confirmation.html"
    # list_filter = ("vendordomain__status",)
    list_filter = (NonCuratedDomains,)
    search_fields = ("name",)
    fields = (
        "nb_antibodies",
        "recent_antibodies",
        "name",
        "nif_id",
        "eu_id",
        "commercial_type",
    )
    readonly_fields = ("nb_antibodies", "recent_antibodies")
    inlines = [
        VendorSynonymInline,
        VendorDomainInline,
    ]

    @admin.display(description="Number of antibodies")
    def nb_antibodies(self, obj):
        return len(Antibody.objects.filter(vendor=obj))

    @admin.display(description=format_html("Recent antibodies<br/>(in queue)"))
    def recent_antibodies(self, obj, limit=10):
        antibodies = Antibody.objects.filter(vendor=obj, status=STATUS.QUEUE)
        # size = len(antibodies)
        if not antibodies.exists():
            return "None"
        return format_html_join(
            "\n", "<li>{}</li>", ((id_with_ab(a),) for a in antibodies)
        )

    def delete_view(self, request, object_id, extra_context=None):
        extra_context = extra_context or {}
        extra_context["vendors"] = list(self.model.objects.filter(~Q(id=object_id)))
        extra_context["nb_antibodies"] = list(Antibody.objects.filter(vendor=object_id))
        return super().delete_view(
            request,
            object_id,
            extra_context,
        )

    def _force_delete(self, src_vendor: Vendor):
        # We make copies of the iterables, just in case
        to_delete = [a for a in src_vendor.antibody_set.all()]
        to_delete.extend(d for d in src_vendor.vendordomain_set.all())
        for entity in to_delete:
            entity.delete()

    def _swap_ownership(self, src_vendor, target_vendor):
        # We transfer the antibodies to the new vendor
        target_vendor.antibody_set.set(src_vendor.antibody_set.all())
        target_vendor.vendordomain_set.set(src_vendor.vendordomain_set.all())
        src_vendor.antibody_set.remove()
        src_vendor.vendordomain_set.remove()

        # We save the updated model
        src_vendor.save()
        target_vendor.save()

    def get_deleted_objects(self, objs, request):
        if request.method == "POST":
            if not objs:
                return super().get_deleted_objects(objs, request)
            src_vendor = objs[0]
            # This case is only for deleting single vendor
            if "_swap_ownership" in request.POST:
                target_vendor = self.model.objects.filter(
                    id=request._post["vendors"]
                ).first()
                self._swap_ownership(src_vendor, target_vendor)
                return super().get_deleted_objects(objs, request)
            # This case if for deleting a vendor, forcing antibody deletion also
            if "_force_delete" in request.POST:
                self._force_delete(src_vendor)
                return super().get_deleted_objects(objs, request)
        return super().get_deleted_objects(objs, request)


# admin.site.register(VendorSynonym)
