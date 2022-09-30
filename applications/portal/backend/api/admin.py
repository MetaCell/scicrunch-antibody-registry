from django.contrib import admin

from api.models import Antibody, Gene, Vendor, Specie, VendorDomain, VendorSynonym

admin.site.register(Antibody)
admin.site.register(Gene)
admin.site.register(Vendor)
admin.site.register(Specie)
admin.site.register(VendorDomain)
admin.site.register(VendorSynonym)
