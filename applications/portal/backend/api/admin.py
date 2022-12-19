from django.contrib import admin
from import_export.admin import ImportMixin

from api.forms.AntibodyImportForm import AntibodyImportForm
from api.models import Antibody, Application, Gene, Vendor, Specie, VendorDomain, VendorSynonym
from api.resources.AntibodyResource import AntibodyResource
from areg_portal.settings import FOR_NEW_KEY, FOR_EXTANT_KEY, METHOD_KEY


@admin.register(Antibody)
class AntibodyAdmin(ImportMixin, admin.ModelAdmin):

    import_template_name = 'admin/import_export/custom_import_form.html'

    # todo set tmp_storage_class
    # https://django-import-export.readthedocs.io/en/latest/getting_started.html#import-confirmation
    import_form_class = AntibodyImportForm
    resource_classes = [AntibodyResource]

    list_filter = ('status',)
    search_fields = ('ab_id', 'ab_name', 'catalog_num')
    list_display = ('ab_id', 'ab_name', 'status')
    autocomplete_fields = ['vendor', 'antigen', 'species', 'source_organism']

    def get_resource_kwargs(self, request, *args, **kwargs):
        rk = super().get_resource_kwargs(request, *args, **kwargs)
        rk['request'] = request
        return rk

    def get_import_data_kwargs(self, request, *args, **kwargs):
        kwargs[FOR_NEW_KEY] = request.POST.get(FOR_NEW_KEY, None)
        kwargs[FOR_EXTANT_KEY] = request.POST.get(FOR_EXTANT_KEY, None)
        kwargs[METHOD_KEY] = request.POST.get(METHOD_KEY, None)
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
