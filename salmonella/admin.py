from django.contrib import admin

from salmonella.widgets import SalmonellaIdWidget, SalmonellaMultiIdWidget

class SalmonellaModelAdmin(admin.ModelAdmin):
    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name in self.salmonella_fields:
            kwargs.pop("request", None)
            type = db_field.rel.__class__.__name__
            if type == "ManyToOneRel" or type == "OneToOneRel":
                kwargs['widget'] = SalmonellaIdWidget(db_field.rel)
            elif type == "ManyToManyRel":
                kwargs['widget'] = SalmonellaMultiIdWidget(db_field.rel)
            return db_field.formfield(**kwargs)
        return super(SalmonellaModelAdmin, self).formfield_for_dbfield(db_field, **kwargs)