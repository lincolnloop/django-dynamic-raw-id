from dynamic_raw_id.widgets import DynamicRawIDWidget, DynamicRawIDMultiIdWidget
from django import VERSION


class DynamicRawIDMixin(object):
    dynamic_raw_id_fields = ()

    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
        if db_field.name in self.dynamic_raw_id_fields:
            rel = db_field.remote_field if VERSION[0] == 2 else db_field.rel
            kwargs['widget'] = DynamicRawIDWidget(rel, self.admin_site)
            return db_field.formfield(**kwargs)
        return super(DynamicRawIDMixin, self).formfield_for_foreignkey(
            db_field, request, **kwargs)

    def formfield_for_manytomany(self, db_field, request=None, **kwargs):
        if db_field.name in self.dynamic_raw_id_fields:
            rel = db_field.remote_field if VERSION[0] == 2 else db_field.rel
            kwargs['widget'] = DynamicRawIDMultiIdWidget(rel, self.admin_site)
            kwargs['help_text'] = ''
            return db_field.formfield(**kwargs)
        return super(DynamicRawIDMixin, self).formfield_for_manytomany(
            db_field, request, **kwargs)
