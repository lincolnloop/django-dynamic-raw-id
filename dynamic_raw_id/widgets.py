from django.conf import settings
from django.contrib.admin import widgets
from django.core.exceptions import ImproperlyConfigured
from django.template.loader import render_to_string
from django.utils.encoding import force_text
from django import VERSION

try:
    from django.urls import reverse, NoReverseMatch
except ImportError:
    from django.core.urlresolvers import reverse, NoReverseMatch


class DynamicRawIDImproperlyConfigured(ImproperlyConfigured):
    pass


class DynamicRawIDWidget(widgets.ForeignKeyRawIdWidget):
    template_name = 'dynamic_raw_id/admin/widgets/dynamic_raw_id_field_dj111.html'

    def render(self, name, value, attrs=None, multi=False):
        """
        Django <= 1.10 variant.
        """
        if (VERSION[0] == 1 and VERSION[1] >= 11) or (VERSION[0] >= 2):
            return super(DynamicRawIDWidget, self).render(name, value, attrs, renderer=None)

        if attrs is None:
            attrs = {}

        related_url = reverse('admin:%s_%s_changelist' % (
            self.rel.to._meta.app_label,
            self.rel.to._meta.object_name.lower()),
            current_app=self.admin_site.name)

        params = self.url_parameters()
        if params:
            url = u'?' + u'&'.join([u'%s=%s' % (k, v) for k, v in params.items()])
        else:
            url = u''
        if "class" not in attrs:
            attrs['class'] = 'vForeignKeyRawIdAdminField'  # The JavaScript looks for this hook.
        app_name = self.rel.to._meta.app_label.strip()
        model_name = self.rel.to._meta.object_name.lower().strip()
        hidden_input = super(widgets.ForeignKeyRawIdWidget, self).render(name, value, attrs)

        extra_context = {
            'hidden_input': hidden_input,
            'name': name,
            'app_name': app_name,
            'model_name': model_name,
            'related_url': related_url,
            'url': url,
        }
        return render_to_string('dynamic_raw_id/admin/widgets/dynamic_raw_id_field.html',
                                extra_context)

    def get_context(self, name, value, attrs):
        """
        Django >= 1.11 variant.
        """
        context = super(DynamicRawIDWidget, self).get_context(name, value, attrs)
        model = self.rel.model if VERSION[0] == 2 else self.rel.to
        related_url = reverse('admin:%s_%s_changelist' % (
            model._meta.app_label,
            model._meta.object_name.lower()),
            current_app=self.admin_site.name)

        params = self.url_parameters()
        if params:
            url = u'?' + u'&'.join([u'%s=%s' % (k, v) for k, v in params.items()])
        else:
            url = u''
        if "class" not in attrs:
            attrs['class'] = 'vForeignKeyRawIdAdminField'  # The JavaScript looks for this hook.
        app_name = model._meta.app_label.strip()
        model_name = model._meta.object_name.lower().strip()

        context.update({
            'name': name,
            'app_name': app_name,
            'model_name': model_name,
            'related_url': related_url,
            'url': url,
        })
        return context

    class Media:
        js = ("dynamic_raw_id/js/dynamic_raw_id.js",)


class DynamicRawIDMultiIdWidget(DynamicRawIDWidget):
    def value_from_datadict(self, data, files, name):
        value = data.get(name)
        if value:
            return value.split(',')

    def render(self, name, value, attrs):
        attrs['class'] = 'vManyToManyRawIdAdminField'
        value = ','.join([force_text(v) for v in value]) if value else ''
        return super(DynamicRawIDMultiIdWidget, self).render(name, value, attrs)
