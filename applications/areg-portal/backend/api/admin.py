from django.contrib import admin

from api.models import Antibody, Antigen, AntigenModification, AntigenSpecie, Vendor, CatalogAlternative, Catalog

admin.site.register(Antibody)
admin.site.register(Antigen)
admin.site.register(AntigenModification)
admin.site.register(AntigenSpecie)
admin.site.register(Vendor)
admin.site.register(Catalog)
admin.site.register(CatalogAlternative)
