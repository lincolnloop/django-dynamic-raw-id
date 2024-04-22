from django.urls import path

from .views import LabelView, MultiLabelView

app_name = "dynamic_raw_id"

urlpatterns = [
    path(
        "<slug:app_name>/<slug:model_name>/multiple/",
        MultiLabelView.as_view(),
        name="dynamic_raw_id_multi_label",
    ),
    path(
        "<slug:app_name>/<slug:model_name>/",
        LabelView.as_view(),
        name="dynamic_raw_id_label",
    ),
]
