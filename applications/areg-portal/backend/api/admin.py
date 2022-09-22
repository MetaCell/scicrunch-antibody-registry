from django.contrib import admin

from api.models import Antibody, Gene, Vendor

admin.site.register(Antibody)
admin.site.register(Gene)
admin.site.register(Vendor)
