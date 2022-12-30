from django.contrib.admin import site as default_admin_site
from django.urls import path

from dynamic_raw_id.views import label_view

app_name = 'dynamic_raw_id'

def get_urls(admin_site=default_admin_site):
    urlpatterns = [
        path(
            "<slug:app_name>/<slug:model_name>/multiple/",
            label_view,
            {
                "multi": True,
                "template_object_name": "objects",
                "template_name": "dynamic_raw_id/multi_label.html",
                "admin_site": admin_site
            },
            name="dynamic_raw_id_multi_label",
        ),
        path(
            "<slug:app_name>/<slug:model_name>/",
            label_view,
            {
                "template_name": "dynamic_raw_id/label.html",
                "admin_site": admin_site
            },
            name="dynamic_raw_id_label",
        ),
    ]

    return urlpatterns

urlpatterns = get_urls()
