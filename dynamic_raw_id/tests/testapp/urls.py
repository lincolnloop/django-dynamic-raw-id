from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/dynamic_raw_id/", include("dynamic_raw_id.urls")),
    path("admin/", admin.site.urls),
]
