from django.contrib import admin
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.db.models import get_model
from django.conf.urls.defaults import patterns, url

from salmonella.widgets import SalmonellaIdWidget, SalmonellaMultiIdWidget

class SalmonellaModelAdmin(admin.ModelAdmin):
    def get_urls(self):
        urls = super(SalmonellaModelAdmin, self).get_urls()
        salmonella_urls = patterns('',
            url(r'^salmonella/(?P<app_name>[\w-]+)/(?P<model_name>[\w-]+)/multiple/$',
                self.admin_site.admin_view(self.label_view), {
                    'multi': True,
                    'template_object_name': 'objects',
                    'template_name': 'salmonella/multi_label.html'
            }, name="salmonella_multi_label"),
            url(r'^salmonella/(?P<app_name>[\w-]+)/(?P<model_name>[\w-]+)/$',
                self.admin_site.admin_view(self.label_view), {
                    'template_name': 'salmonella/label.html'
            }, name="salmonella_label"),
        )
        
        return salmonella_urls + urls

    def label_view(self, request, app_name, model_name, template_name="", multi=False,
                   template_object_name="object"):
        object_id = request.GET.get("id", "")
        model = get_model(app_name, model_name)
        try:
            if multi:
                if object_id:
                    object_id = object_id.split(",")
                model_template = "salmanella/%s/multi_%s.html" % (app_name, model_name)
                obj = model.objects.filter(id__in=object_id)
            else:
                model_template = "salmanella/%s/%s.html" % (app_name, model_name)
                obj = model.objects.get(id=object_id)
        except model.DoesNotExist:
            return HttpResponse("")
        return render_to_response((model_template, template_name),
                                  {template_object_name: obj})
        
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