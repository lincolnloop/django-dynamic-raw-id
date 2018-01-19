from django.conf.urls import *
from dynamic_raw_id.views import label_view

urlpatterns = [
    url(r'^(?P<app_name>[\w-]+)/(?P<model_name>[\w-]+)/multiple/$',
        label_view,
        {
            'multi': True,
            'template_object_name': 'objects',
            'template_name': 'dynamic_raw_id/multi_label.html'
        },
        name="dynamic_raw_id_multi_label"),
    url(r'^(?P<app_name>[\w-]+)/(?P<model_name>[\w-]+)/$',
        label_view,
        {
            'template_name': 'dynamic_raw_id/label.html'
        },
        name="dynamic_raw_id_label"),
]
