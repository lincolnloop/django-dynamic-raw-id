from django.contrib import admin

from salmonella.admin import SalmonellaMixin

from .models import SalmonellaTest


class SalmonellaTestAdmin(SalmonellaMixin, admin.ModelAdmin):
    salmonella_fields = ('user', 'staff_member')


admin.site.register(SalmonellaTest, SalmonellaTestAdmin)
