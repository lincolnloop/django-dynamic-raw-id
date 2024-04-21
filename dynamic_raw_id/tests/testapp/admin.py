from django.contrib import admin

from dynamic_raw_id.admin import DynamicRawIDMixin
from dynamic_raw_id.filters import DynamicRawIDFilter

from . import models


@admin.register(models.ModelToTest)
class ModelToTestAdmin(DynamicRawIDMixin, admin.ModelAdmin):
    raw_id_fields = (
        "rawid_fk",
        "rawid_fk_limited",
        "rawid_many",
    )
    dynamic_raw_id_fields = (
        "dynamic_raw_id_fk",
        "dynamic_raw_id_fk_limited",
        "dynamic_raw_id_many",
        "dynamic_raw_id_fk_int_pk",
        "dynamic_raw_id_fk_char_pk",
        "dynamic_raw_id_fk_uuid_pk",
    )
    list_filter = (
        ("dynamic_raw_id_fk", DynamicRawIDFilter),
        ("dynamic_raw_id_fk_int_pk", DynamicRawIDFilter),
        ("dynamic_raw_id_fk_char_pk", DynamicRawIDFilter),
        ("dynamic_raw_id_fk_uuid_pk", DynamicRawIDFilter),
    )


class ModelToTestInlineAdmin(DynamicRawIDMixin, admin.TabularInline):
    model = models.ModelToTestInlines
    dynamic_raw_id_fields = (
        "dynamic_raw_id_fk",
        "dynamic_raw_id_fk_limited",
        "dynamic_raw_id_many",
        "dynamic_raw_id_fk_int_pk",
        "dynamic_raw_id_fk_char_pk",
        "dynamic_raw_id_fk_uuid_pk",
    )


@admin.register(models.ModelToTestInlinesBase)
class ModelToTestInlineBaseAdmin(admin.ModelAdmin):
    inlines = (ModelToTestInlineAdmin,)


admin.site.register(models.IntPrimaryKeyModel)
admin.site.register(models.CharPrimaryKeyModel)
admin.site.register(models.UUIDPrimaryKeyModel)
