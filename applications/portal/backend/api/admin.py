from django.contrib import admin
from django.utils.html import format_html, format_html_join

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
class AntibodyAdmin(admin.ModelAdmin):
    list_filter = ("status",)
    list_display = (id_with_ab, "ab_name", "status")
    search_fields = ("ab_id", "ab_name", "catalog_num")
    # readonly_fields = ("ab_id", "catalog_num", "accession")
    autocomplete_fields = ("vendor", "antigen", "species", "source_organism")
    inlines = (AntibodySpeciesInline, AntibodyApplicationsInline)


@admin.register(Gene)
class GeneAdmin(admin.ModelAdmin):
    search_fields = ("symbol", "entrez_id", "uniprot_id")


@admin.register(Specie)
class SpecieAdmin(admin.ModelAdmin):
    search_fields = ("name",)


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    search_fields = ("name",)


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


@admin.register(VendorDomain)
class VendorDomainAdmin(admin.ModelAdmin):
    list_display = (
        "base_url",
        "vendor",
        "status",
        "is_domain_visible",
    )
    list_editable = ("is_domain_visible",)


@admin.register(Vendor)
class VendorAdmin(admin.ModelAdmin):
    list_filter = ("vendordomain__status",)
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


admin.site.register(VendorSynonym)
