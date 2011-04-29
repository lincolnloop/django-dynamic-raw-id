from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.db.models import get_model
from django.conf.urls.defaults import patterns, url

from salmonella.widgets import SalmonellaIdWidget, SalmonellaMultiIdWidget

class SalmonellaModelAdminMixin(object):
    salmonella_fields = ()
    
    def get_urls(self):
        urls = super(SalmonellaModelAdminMixin, self).get_urls()
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
                model_template = "salmonella/%s/multi_%s.html" % (app_name, model_name)
                obj = model.objects.filter(id__in=object_id)
            else:
                model_template = "salmonella/%s/%s.html" % (app_name, model_name)
                obj = model.objects.get(id=object_id)
        except model.DoesNotExist:
            return HttpResponse("")
        return render_to_response((model_template, template_name),
                                  {template_object_name: obj})
    
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