from django.contrib import admin

from dynamic_rawid.admin import dynamic_rawidMixin
from dynamic_rawid.filters import dynamic_rawidFilter

from .models import dynamic_rawidTest, DirectPrimaryKeyModel, CharPrimaryKeyModel


class dynamic_rawidTestAdmin(dynamic_rawidMixin, admin.ModelAdmin):
    raw_id_fields = (
        'rawid_fk',
        'rawid_fk_limited',
        'rawid_many'
    )
    dynamic_rawid_fields = (
        'dynamic_rawid_fk',
        'dynamic_rawid_fk_limited',
        'dynamic_rawid_many',
        'dynamic_rawid_fk_direct_pk',
        'dynamic_rawid_fk_char_pk'
    )
    list_filter = (
        ('dynamic_rawid_fk', dynamic_rawidFilter),
    )

admin.site.register(DirectPrimaryKeyModel)
admin.site.register(CharPrimaryKeyModel)
admin.site.register(dynamic_rawidTest, dynamic_rawidTestAdmin)
