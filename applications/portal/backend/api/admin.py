from django.contrib import admin

from api.models import Antibody, Gene, Vendor, Specie, VendorDomain, VendorSynonym


class AntibodyAdmin(admin.ModelAdmin):
    list_filter = ('status',)
    search_fields = ('ab_id', 'ab_name', 'catalog_num')
    list_display = ('ab_id', 'ab_name', 'status')
    autocomplete_fields = ['vendor', 'antigen', 'species', 'source_organism']


admin.site.register(Antibody, AntibodyAdmin)
admin.site.register(Gene)
admin.site.register(Vendor)
admin.site.register(Specie)
admin.site.register(VendorDomain)
admin.site.register(VendorSynonym)
