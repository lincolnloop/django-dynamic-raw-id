from salmonella.widgets import SalmonellaIdWidget, SalmonellaMultiIdWidget


class SalmonellaMixin(object):
    salmonella_fields = ()

    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
        if db_field.name in self.salmonella_fields:
            try:
                kwargs['widget'] = SalmonellaIdWidget(db_field.rel)
            except TypeError:  # django 1.4+
                kwargs['widget'] = SalmonellaIdWidget(db_field.rel, self.admin_site)
            return db_field.formfield(**kwargs)
        return super(SalmonellaMixin, self).formfield_for_foreignkey(db_field,
                                                                     request,
                                                                     **kwargs)

    def formfield_for_manytomany(self, db_field, request=None, **kwargs):
        if db_field.name in self.salmonella_fields:
            try:
                kwargs['widget'] = SalmonellaMultiIdWidget(db_field.rel)
            except TypeError:  # django 1.4+
                kwargs['widget'] = SalmonellaIdWidget(db_field.rel, self.admin_site)
            kwargs['help_text'] = ''
            return db_field.formfield(**kwargs)
        return super(SalmonellaMixin, self).formfield_for_manytomany(db_field,
                                                                     request,
                                                                     **kwargs)
