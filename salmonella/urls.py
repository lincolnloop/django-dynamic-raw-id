from django.conf.urls.defaults import *

urlpatterns = patterns('salmonella.views',
    url(r'^(?P<app_name>[\w-]+)/(?P<model_name>[\w-]+)/multiple/$',
        'label', {'multi': True,
                  'template_object_name': 'objects',
                  'template_name': 'salmonella/multi_label.html'},
        name="salmanella_multi_label"),
    url(r'^(?P<app_name>[\w-]+)/(?P<model_name>[\w-]+)/$',
        'label', {'template_name': 'salmonella/label.html'},
        name="salmanella_label"),
)
