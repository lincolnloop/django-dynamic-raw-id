from django.conf.urls import *
from dynamic_rawid.views import label_view

urlpatterns = [
    url(r'^(?P<app_name>[\w-]+)/(?P<model_name>[\w-]+)/multiple/$',
        label_view,
        {
            'multi': True,
            'template_object_name': 'objects',
            'template_name': 'dynamic_rawid/multi_label.html'
        },
        name="dynamic_rawid_multi_label"),
    url(r'^(?P<app_name>[\w-]+)/(?P<model_name>[\w-]+)/$',
        label_view,
        {
            'template_name': 'dynamic_rawid/label.html'
        },
        name="dynamic_rawid_label"),
]
