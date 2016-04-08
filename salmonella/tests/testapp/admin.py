from django.contrib import admin

from salmonella.admin import SalmonellaMixin
from salmonella.filters import SalmonellaFilter

from .models import SalmonellaTest, DirectPrimaryKeyModel, CharPrimaryKeyModel


class SalmonellaTestAdmin(SalmonellaMixin, admin.ModelAdmin):
    raw_id_fields = (
        'rawid_fk',
        'rawid_fk_limited',
        'rawid_many'
    )
    salmonella_fields = (
        'salmonella_fk',
        'salmonella_fk_limited',
        'salmonella_many',
        'salmonella_fk_direct_pk',
        'salmonella_fk_char_pk'
    )
    list_filter = (
        ('salmonella_fk', SalmonellaFilter),
    )

admin.site.register(DirectPrimaryKeyModel)
admin.site.register(CharPrimaryKeyModel)
admin.site.register(SalmonellaTest, SalmonellaTestAdmin)
