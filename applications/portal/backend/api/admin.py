from django.contrib import admin
from django.utils.html import format_html, format_html_join

from api.models import (
    Antibody,
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


@admin.register(Antibody)
class AntibodyAdmin(admin.ModelAdmin):
    list_filter = ("status",)
    search_fields = ("ab_id", "ab_name", "catalog_num")
    list_display = (id_with_ab, "ab_name", "status")
    autocomplete_fields = ["vendor", "antigen", "species", "source_organism"]


@admin.register(Vendor)
class VendorAdmin(admin.ModelAdmin):
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

    @admin.display(description="Number of antibodies")
    def nb_antibodies(self, obj):
        return len(Antibody.objects.filter(vendor=obj))

    @admin.display(description="Recent antibodies")
    def recent_antibodies(self, obj, limit=10):
        antibodies = Antibody.objects.filter(vendor=obj).order_by("insert_time")[:10]
        return format_html_join(
            "\n", "<li>{}</li>", ((f"AB_{a.ab_id}",) for a in antibodies)
        )


@admin.register(Gene)
class GeneAdmin(admin.ModelAdmin):
    search_fields = ("symbol", "entrez_id", "uniprot_id")


@admin.register(Specie)
class SpecieAdmin(admin.ModelAdmin):
    search_fields = ("name",)


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    search_fields = ("name",)


@admin.register(VendorDomain)
class VendorDomainAdmin(admin.ModelAdmin):
    list_display = (
        "base_url",
        "vendor",
        "status",
        "is_domain_visible",
    )
    list_editable = ("is_domain_visible",)


admin.site.register(VendorSynonym)
