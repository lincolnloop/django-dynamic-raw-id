from django.conf.urls import url

from views import dynamic_label_view

def get_url_patterns(admin_site='admin'):
    return [
        url(r'^(?P<app_name>[\w-]+)/(?P<model_name>[\w-]+)/multiple/$',
            dynamic_label_view(admin_site),
            {
                'multi': True,
                'template_object_name': 'objects',
                'template_name': 'dynamic_raw_id/multi_label.html'
            },
            name='dynamic_raw_id_multi_label'),
        url(r'^(?P<app_name>[\w-]+)/(?P<model_name>[\w-]+)/$',
            dynamic_label_view(admin_site),
            {
                'template_name': 'dynamic_raw_id/label.html'
            },
            name='dynamic_raw_id_label'),
    ]
