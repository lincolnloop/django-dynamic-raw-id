from django.conf.urls.defaults import patterns, include
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = patterns('',
    (r'', include('project_example.urls')),
)

if settings.MEDIA_ROOT:
    urlpatterns += static(settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT)
