from salmonella.widgets import SalmonellaIdWidget, SalmonellaMultiIdWidget
from django import VERSION


class SalmonellaMixin(object):
    salmonella_fields = ()

    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
        if db_field.name in self.salmonella_fields:

            if VERSION[0] == 2:
                rel = db_field.remote_field
            else:
                rel = db_field.rel

            kwargs['widget'] = SalmonellaIdWidget(rel, self.admin_site)
            return db_field.formfield(**kwargs)
        return super(SalmonellaMixin, self).formfield_for_foreignkey(
            db_field, request, **kwargs)

    def formfield_for_manytomany(self, db_field, request=None, **kwargs):
        if db_field.name in self.salmonella_fields:

            if VERSION[0] == 2:
                rel = db_field.remote_field
            else:
                rel = db_field.rel

            kwargs['widget'] = SalmonellaMultiIdWidget(rel, self.admin_site)
            kwargs['help_text'] = ''
            return db_field.formfield(**kwargs)
        return super(SalmonellaMixin, self).formfield_for_manytomany(db_field,
                                                                     request,
                                                                     **kwargs)
