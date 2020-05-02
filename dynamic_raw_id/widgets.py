from django import VERSION, forms
from django.conf import settings
from django.contrib.admin import widgets
from django.core.exceptions import ImproperlyConfigured
from django.urls import reverse
from django.utils.encoding import force_text


class DynamicRawIDImproperlyConfigured(ImproperlyConfigured):
    pass


class DynamicRawIDWidget(widgets.ForeignKeyRawIdWidget):
    template_name = 'dynamic_raw_id/admin/widgets/dynamic_raw_id_field.html'

    def get_context(self, name, value, attrs):
        context = super(DynamicRawIDWidget, self).get_context(
            name, value, attrs
        )
        model = self.rel.model if VERSION[0] >= 2 else self.rel.to
        related_url = reverse(
            'admin:{0}_{1}_changelist'.format(
                model._meta.app_label, model._meta.object_name.lower()
            ),
            current_app=self.admin_site.name,
        )

        params = self.url_parameters()
        if params:
            url = u'?' + u'&'.join(
                [u'{0}={1}'.format(k, v) for k, v in params.items()]
            )
        else:
            url = u''
        if "class" not in attrs:
            attrs[
                'class'
            ] = 'vForeignKeyRawIdAdminField'  # The JavaScript looks for this hook.
        app_name = model._meta.app_label.strip()
        model_name = model._meta.object_name.lower().strip()

        context.update(
            {
                'name': name,
                'app_name': app_name,
                'model_name': model_name,
                'related_url': related_url,
                'url': url,
            }
        )
        return context

    @property
    def media(self):
        extra = '' if settings.DEBUG else '.min'
        return forms.Media(
            js=[
                'admin/js/vendor/jquery/jquery{0}.js'.format(extra),
                'admin/js/jquery.init.js',
                'admin/js/core.js',
                "dynamic_raw_id/js/dynamic_raw_id.js",
            ]
        )


class DynamicRawIDMultiIdWidget(DynamicRawIDWidget):
    def value_from_datadict(self, data, files, name):
        value = data.get(name)
        if value:
            return value.split(u',')

    def render(self, name, value, attrs, renderer=None):
        attrs['class'] = 'vManyToManyRawIdAdminField'
        value = u','.join([force_text(v) for v in value]) if value else ''
        return super(DynamicRawIDMultiIdWidget, self).render(
            name, value, attrs, renderer=renderer
        )
