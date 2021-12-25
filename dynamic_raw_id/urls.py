from django.urls import re_path

from dynamic_raw_id.views import label_view

urlpatterns = [
    re_path(
        r"^(?P<app_name>[\w-]+)/(?P<model_name>[\w-]+)/multiple/$",
        label_view,
        {
            "multi": True,
            "template_object_name": "objects",
            "template_name": "dynamic_raw_id/multi_label.html",
        },
        name="dynamic_raw_id_multi_label",
    ),
    re_path(
        r"^(?P<app_name>[\w-]+)/(?P<model_name>[\w-]+)/$",
        label_view,
        {"template_name": "dynamic_raw_id/label.html"},
        name="dynamic_raw_id_label",
    ),
]
