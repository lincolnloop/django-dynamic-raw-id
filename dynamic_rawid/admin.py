from dynamic_rawid.widgets import dynamic_rawidIdWidget, dynamic_rawidMultiIdWidget
from django import VERSION


class dynamic_rawidMixin(object):
    dynamic_rawid_fields = ()

    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
        if db_field.name in self.dynamic_rawid_fields:

            if VERSION[0] == 2:
                rel = db_field.remote_field
            else:
                rel = db_field.rel

            kwargs['widget'] = dynamic_rawidIdWidget(rel, self.admin_site)
            return db_field.formfield(**kwargs)
        return super(dynamic_rawidMixin, self).formfield_for_foreignkey(
            db_field, request, **kwargs)

    def formfield_for_manytomany(self, db_field, request=None, **kwargs):
        if db_field.name in self.dynamic_rawid_fields:

            if VERSION[0] == 2:
                rel = db_field.remote_field
            else:
                rel = db_field.rel

            kwargs['widget'] = dynamic_rawidMultiIdWidget(rel, self.admin_site)
            kwargs['help_text'] = ''
            return db_field.formfield(**kwargs)
        return super(dynamic_rawidMixin, self).formfield_for_manytomany(db_field,
                                                                     request,
                                                                     **kwargs)
