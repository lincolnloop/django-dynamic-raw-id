# coding: utf-8

"""dynamic_raw_id filters."""

from django import forms
from django.contrib import admin
from django import VERSION
from dynamic_raw_id.widgets import DynamicRawIDWidget


class DynamicRawIDFilterForm(forms.Form):

    """Form for dynamic_raw_id filter."""

    def __init__(self, rel, admin_site, field_name, **kwargs):
        """Construct field for given field rel."""
        super(DynamicRawIDFilterForm, self).__init__(**kwargs)
        self.fields['%s' % field_name] = forms.IntegerField(
            label='', widget=DynamicRawIDWidget(
                rel=rel, admin_site=admin_site), required=False)


class DynamicRawIDFilter(admin.filters.FieldListFilter):

    """Filter list queryset by primary key of related object."""

    template = 'dynamic_raw_id/admin/filters/dynamic_raw_id_filter.html'

    def __init__(self, field, request, params, model, model_admin, field_path):
        """Use GET param for lookup and form initialization."""
        self.lookup_kwarg = '%s' % field_path
        super(DynamicRawIDFilter, self).__init__(
            field, request, params, model, model_admin, field_path)
        rel = field.remote_field if VERSION[0] == 2 else field.rel
        self.form = self.get_form(request, rel, model_admin.admin_site)

    def choices(self, cl):
        """Filter choices are not available."""
        return []

    def expected_parameters(self):
        """Return GET params for this filter."""
        return [self.lookup_kwarg]

    def get_form(self, request, rel, admin_site):
        """Return filter form."""
        return DynamicRawIDFilterForm(
            admin_site=admin_site, rel=rel, field_name=self.field_path,
            data=self.used_parameters)

    def queryset(self, request, queryset):
        """Filter queryset using params from the form."""
        if self.form.is_valid():
            # get no null params
            filter_params = dict(
                filter(lambda x: bool(x[1]), self.form.cleaned_data.items()))
            return queryset.filter(**filter_params)
        return queryset
