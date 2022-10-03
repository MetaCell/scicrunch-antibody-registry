from django.contrib import admin

from api.models import Antibody, Gene, Vendor, Specie, VendorDomain, VendorSynonym


class AntibodyAdmin(admin.ModelAdmin):
    list_filter = ('status',)
    search_fields = ('ab_id', 'ab_name', 'catalog_num')
    list_display = ('ab_id', 'ab_name', 'status')
    autocomplete_fields = ['vendor', 'antigen', 'species', 'source_organism']


class VendorAdmin(admin.ModelAdmin):
    search_fields = ('name', )


class GeneAdmin(admin.ModelAdmin):
    search_fields = ('symbol', 'entrez_id', 'uniprot_id')


class SpecieAdmin(admin.ModelAdmin):
    search_fields = ('name', )


admin.site.register(Antibody, AntibodyAdmin)
admin.site.register(Gene, GeneAdmin)
admin.site.register(Vendor, VendorAdmin)
admin.site.register(Specie, SpecieAdmin)
admin.site.register(VendorDomain)
admin.site.register(VendorSynonym)
