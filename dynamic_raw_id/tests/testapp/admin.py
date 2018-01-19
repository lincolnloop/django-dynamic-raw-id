from django.contrib import admin

from dynamic_raw_id.admin import DynamicRawIDMixin
from dynamic_raw_id.filters import DynamicRawIDFilter

from .models import TestModel, DirectPrimaryKeyModel, CharPrimaryKeyModel


class TestModelAdmin(DynamicRawIDMixin, admin.ModelAdmin):
    raw_id_fields = (
        'rawid_fk',
        'rawid_fk_limited',
        'rawid_many'
    )
    dynamic_raw_id_fields = (
        'dynamic_raw_id_fk',
        'dynamic_raw_id_fk_limited',
        'dynamic_raw_id_many',
        'dynamic_raw_id_fk_direct_pk',
        'dynamic_raw_id_fk_char_pk'
    )
    list_filter = (
        ('dynamic_raw_id_fk', DynamicRawIDFilter),
    )

admin.site.register(DirectPrimaryKeyModel)
admin.site.register(CharPrimaryKeyModel)
admin.site.register(TestModel, TestModelAdmin)
