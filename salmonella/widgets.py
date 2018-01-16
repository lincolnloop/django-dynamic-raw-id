from django.conf import settings
from django.contrib.admin import widgets
from django.core.exceptions import ImproperlyConfigured
from django.template.loader import render_to_string
from django import VERSION

try:
    from django.urls import reverse, NoReverseMatch
except ImportError:
    from django.core.urlresolvers import reverse, NoReverseMatch

try:
    from django.utils.encoding import force_text
except ImportError:
    from django.utils.encoding import force_unicode as force_text


class SalmonellaImproperlyConfigured(ImproperlyConfigured):
    pass


class SalmonellaIdWidget(widgets.ForeignKeyRawIdWidget):
    template_name = 'salmonella/admin/widgets/salmonella_field_dj111.html'

    def render(self, name, value, attrs=None, multi=False):
        """
        Django <= 1.10 variant.
        """
        if (VERSION[0] == 1 and VERSION[1] >= 11) or (VERSION[0] >= 2):
            return super(SalmonellaIdWidget, self).render(name, value, attrs, renderer=None)

        if attrs is None:
            attrs = {}

        try:
            related_url = reverse('admin:%s_%s_changelist' % (
                self.rel.to._meta.app_label,
                self.rel.to._meta.object_name.lower()),
                current_app=self.admin_site.name)
        except NoReverseMatch:
            raise SalmonellaImproperlyConfigured('The model %s.%s is not '
                'registered in the admin.' % (self.rel.to._meta.app_label,
                                              self.rel.to._meta.object_name))

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
            'SALMONELLA_STATIC': settings.STATIC_URL + 'salmonella/'
        }
        return render_to_string('salmonella/admin/widgets/salmonella_field.html',
                                extra_context)

    def get_context(self, name, value, attrs):
        """
        Django >= 1.11 variant.
        """
        context = super(SalmonellaIdWidget, self).get_context(name, value, attrs)

        model = None
        if (VERSION[0] == 2):
            model = self.rel.model
        else:
            model = self.rel.to

        try:
            related_url = reverse('admin:%s_%s_changelist' % (
                model._meta.app_label,
                model._meta.object_name.lower()),
                current_app=self.admin_site.name)
        except NoReverseMatch:
            raise SalmonellaImproperlyConfigured('The model %s.%s is not '
                'registered in the admin.' % (model._meta.app_label,
                                              model._meta.object_name))

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
            'SALMONELLA_STATIC': settings.STATIC_URL + 'salmonella/'
        })
        return context

    class Media:
        js = (settings.STATIC_URL + "salmonella/js/salmonella.js",)


class SalmonellaMultiIdWidget(SalmonellaIdWidget):
    def value_from_datadict(self, data, files, name):
        value = data.get(name)
        if value:
            return value.split(',')

    def render(self, name, value, attrs):
        attrs['class'] = 'vManyToManyRawIdAdminField'
        value = ','.join([force_text(v) for v in value]) if value else ''
        return super(SalmonellaMultiIdWidget, self).render(name, value, attrs)
