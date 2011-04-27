from django.conf import settings
from django.contrib.admin import widgets
from django.utils.encoding import force_unicode
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext as _

class SalmonellaIdWidget(widgets.ForeignKeyRawIdWidget):
    def render(self, name, value, attrs=None, multi=False):
        if attrs is None:
            attrs = {}
        related_url = '../../../%s/%s/' % (self.rel.to._meta.app_label, self.rel.to._meta.object_name.lower())
        params = self.url_parameters()
        if params:
            url = u'?' + u'&amp;'.join([u'%s=%s' % (k, v) for k, v in params.items()])
        else:
            url = u''
        if "class" not in attrs:
            attrs['class'] = 'vForeignKeyRawIdAdminField' # The JavaScript looks for this hook.
        app_name = self.rel.to._meta.app_label.strip()
        model_name = self.rel.to._meta.object_name.lower().strip()
        output = [super(widgets.ForeignKeyRawIdWidget, self).render(name, value, attrs)]
        # TODO: "id_" is hard-coded here. This should instead use the correct
        # API to determine the ID dynamically.
        fmt_str = u'<a href="%s%s" data-name="%s" data-app="%s" data-model="%s" class="related-lookup" id="lookup_id_%s" onclick="return popup_wrapper(this);"> '
        output.append(fmt_str % (related_url, url, name, app_name, model_name, name))
        output.append(u'<img src="%simg/admin/selector-search.gif" width="16" height="16" alt="%s" /></a>' % (settings.ADMIN_MEDIA_PREFIX, _('Lookup')))
        if value:
            if multi:
                labels = []
                for i in value.split(","):
                    labels.append(self.label_for_value(i))
                output.append('<span class="salmonella_label" id="%s_salmonella_label">%s</span>' % (name, ",".join(labels)))
            else:
                output.append('<span class="salmonella_label" id="%s_salmonella_label">%s</span>' % (name, self.label_for_value(value)))
        else:
            output.append('<span class="salmonella_label" id="%s_salmonella_label"></span>' % name)
        return mark_safe(u''.join(output))
    
    class Media:
        js = (settings.STATIC_URL + "salmonella.js",)

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
        return super(SalmonellaMultiIdWidget, self).render(name, value, attrs, multi=True)