from django.conf.urls import *
from salmonella.views import label_view

urlpatterns = [
    url(r'^(?P<app_name>[\w-]+)/(?P<model_name>[\w-]+)/multiple/$',
        label_view,
        {
            'multi': True,
            'template_object_name': 'objects',
            'template_name': 'salmonella/multi_label.html'
        },
        name="salmonella_multi_label"),
    url(r'^(?P<app_name>[\w-]+)/(?P<model_name>[\w-]+)/$',
        label_view,
        {
            'template_name': 'salmonella/label.html'
        },
        name="salmonella_label"),
]
