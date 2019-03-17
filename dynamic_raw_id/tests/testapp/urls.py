from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^admin/dynamic_raw_id/', include('dynamic_raw_id.urls')),
]
