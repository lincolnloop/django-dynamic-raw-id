# coding: utf-8

"""Salmonella filters."""

from django import forms
from django.contrib import admin
from salmonella.widgets import SalmonellaIdWidget


class SalmonellaFilterForm(forms.Form):

    """Form for Salmonella filter."""

    def __init__(self, rel, admin_site, field_name, **kwargs):
        """Construct field for given field rel."""
        super(SalmonellaFilterForm, self).__init__(**kwargs)

        self.fields['%s' % field_name] = forms.IntegerField(
            label='', widget=SalmonellaIdWidget(
                rel=rel, admin_site=admin_site), required=False)


class SalmonellaFilter(admin.filters.FieldListFilter):

    """Filter list queryset by primary key of related object."""

    template = 'salmonella/admin/filters/salmonella_filter.html'

    def __init__(self, field, request, params, model, model_admin, field_path):
        """Use GET param for lookup and form initialization."""
        self.lookup_kwarg = '%s' % field_path
        super(SalmonellaFilter, self).__init__(
            field, request, params, model, model_admin, field_path)
        self.form = self.get_form(request, field.rel, model_admin.admin_site)

    def choices(self, cl):
        """Filter choices are not available."""
        return []

    def expected_parameters(self):
        """Return GET params for this filter."""
        return [self.lookup_kwarg]

    def get_form(self, request, rel, admin_site):
        """Return filter form."""
        return SalmonellaFilterForm(admin_site=admin_site, rel=rel,
                                    field_name=self.field_path,
                                    data=self.used_parameters)

    def queryset(self, request, queryset):
        """Filter queryset using params from the form."""
        if self.form.is_valid():
            # get no null params
            filter_params = dict(filter(lambda x: bool(x[1]),
                                        self.form.cleaned_data.items()))
            return queryset.filter(**filter_params)
        else:
            return queryset
