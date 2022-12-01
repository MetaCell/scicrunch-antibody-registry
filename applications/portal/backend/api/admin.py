from django.contrib import admin
from import_export.admin import ImportMixin

from api.forms.AntibodyImportForm import AntibodyImportForm
from api.models import Antibody, Application, Gene, Vendor, Specie, VendorDomain, VendorSynonym
from api.resources.AntibodyResource import AntibodyResource


@admin.register(Antibody)
class AntibodyAdmin(ImportMixin, admin.ModelAdmin):
    # todo set tmp_storage_class
    # https://django-import-export.readthedocs.io/en/latest/getting_started.html#import-confirmation
    import_form_class = AntibodyImportForm
    resource_classes = [AntibodyResource]

    list_filter = ('status',)
    search_fields = ('ab_id', 'ab_name', 'catalog_num')
    list_display = ('ab_id', 'ab_name', 'status')
    autocomplete_fields = ['vendor', 'antigen', 'species', 'source_organism']

    def get_import_data_kwargs(self, request, *args, **kwargs):
        kwargs['for_new'] = request.POST.get('for_new', None)
        kwargs['for_extant'] = request.POST.get('for_extant', None)
        kwargs['method'] = request.POST.get('method', None)
        return super().get_import_data_kwargs(request, *args, **kwargs)


class VendorAdmin(admin.ModelAdmin):
    search_fields = ('name',)


class GeneAdmin(admin.ModelAdmin):
    search_fields = ('symbol', 'entrez_id', 'uniprot_id')


class SpecieAdmin(admin.ModelAdmin):
    search_fields = ('name',)


class ApplicationAdmin(admin.ModelAdmin):
    search_fields = ('name',)


# admin.site.register(Antibody, AntibodyAdmin)
admin.site.register(Gene, GeneAdmin)
admin.site.register(Vendor, VendorAdmin)
admin.site.register(Specie, SpecieAdmin)
admin.site.register(Application, ApplicationAdmin)
admin.site.register(VendorDomain)
admin.site.register(VendorSynonym)
