from django.conf.urls import url, include
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^admin/dynamic_rawid/', include('dynamic_rawid.urls')),
]
