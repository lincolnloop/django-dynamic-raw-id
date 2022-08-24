from dynamic_raw_id.widgets import DynamicRawIDMultiIdWidget, DynamicRawIDWidget


class DynamicRawIDMixin:
    dynamic_raw_id_fields = ()
    dynamic_raw_id_admin_site = 'admin'

    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
        if db_field.name in self.dynamic_raw_id_fields:
            rel = db_field.remote_field
            kwargs['widget'] = DynamicRawIDWidget(
                rel,
                self.admin_site,
                dynamic_raw_id_admin_site=self.dynamic_raw_id_admin_site
            )
            return db_field.formfield(**kwargs)
        return super().formfield_for_foreignkey(
            db_field, request, **kwargs
        )

    def formfield_for_manytomany(self, db_field, request=None, **kwargs):
        if db_field.name in self.dynamic_raw_id_fields:
            rel = db_field.remote_field
            kwargs['widget'] = DynamicRawIDMultiIdWidget(rel, self.admin_site)
            kwargs['help_text'] = ''
            return db_field.formfield(**kwargs)
        return super().formfield_for_manytomany(
            db_field, request, **kwargs
        )
