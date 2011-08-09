from django.conf import settings
from django.contrib.admin import widgets
from django.template.loader import render_to_string
from django.utils.encoding import force_unicode
from django.core.urlresolvers import reverse


class SalmonellaIdWidget(widgets.ForeignKeyRawIdWidget):
    def render(self, name, value, attrs=None, multi=False):
        if attrs is None:
            attrs = {}
        related_url = reverse('admin:%s_%s_changelist' %
                               (self.rel.to._meta.app_label,
                                self.rel.to._meta.object_name.lower()))
        params = self.url_parameters()
        if params:
            url = u'?' + u'&amp;'.join([u'%s=%s' % (k, v) for k, v in params.items()])
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
            'admin_media_prefix': settings.ADMIN_MEDIA_PREFIX,
        }
        return render_to_string('salmonella/admin/widgets/salmonella_field.html',
                                extra_context)

    class Media:
        js = (settings.STATIC_URL + "salmonella/js/salmonella.js",)


class SalmonellaMultiIdWidget(SalmonellaIdWidget):
    def value_from_datadict(self, data, files, name):
        value = data.get(name)
        if value:
            return value.split(',')

    def render(self, name, value, attrs=None):
        if attrs is None:
            attrs = {}
        attrs['class'] = 'vManyToManyRawIdAdminField'
        if value:
            value = ','.join([force_unicode(v) for v in value])
        else:
            value = ''
        return super(SalmonellaMultiIdWidget, self).render(name, value,
                                                           attrs, multi=True)
