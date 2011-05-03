
from salmonella.widgets import SalmonellaIdWidget, SalmonellaMultiIdWidget

class SalmonellaModelAdminMixin(object):
    salmonella_fields = ()
    
    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
        if db_field.name in self.salmonella_fields:
            kwargs['widget'] = SalmonellaIdWidget(db_field.rel)
            return db_field.formfield(**kwargs)
        return super(SalmonellaModelAdminMixin, self).formfield_for_foreignkey(db_field, request, **kwargs)
        
    def formfield_for_manytomany(self, db_field, request=None, **kwargs):
        if db_field.name in self.salmonella_fields:
            kwargs['widget'] = SalmonellaMultiIdWidget(db_field.rel)
            kwargs['help_text'] = ''
            return db_field.formfield(**kwargs)
        return super(SalmonellaModelAdminMixin, self).formfield_for_manytomany(db_field, request, **kwargs)

class SalmonellaTabularInlineMixin(object):
    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
        if db_field.name in self.salmonella_fields:
            kwargs['widget'] = SalmonellaIdWidget(db_field.rel)
            return db_field.formfield(**kwargs)
        return super(SalmonellaTabularInlineMixin, self).formfield_for_foreignkey(db_field, request, **kwargs)
        
    def formfield_for_manytomany(self, db_field, request=None, **kwargs):
        if db_field.name in self.salmonella_fields:
            kwargs['widget'] = SalmonellaMultiIdWidget(db_field.rel)
            kwargs['help_text'] = ''
            return db_field.formfield(**kwargs)
        return super(SalmonellaTabularInlineMixin, self).formfield_for_manytomany(db_field, request, **kwargs)