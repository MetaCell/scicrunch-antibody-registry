from django.contrib import admin

from api.models import Antibody, Antigen, Vendor

admin.site.register(Antibody)
admin.site.register(Antigen)
admin.site.register(Vendor)
