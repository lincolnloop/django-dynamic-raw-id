from __future__ import annotations

from typing import TYPE_CHECKING, Any
from urllib.parse import urlencode

from django import forms
from django.contrib.admin import widgets
from django.urls import reverse
from django.utils.encoding import force_str

if TYPE_CHECKING:
    from django.template import Context


class DynamicRawIDWidget(widgets.ForeignKeyRawIdWidget):
    template_name: str = "dynamic_raw_id/admin/widgets/dynamic_raw_id_field.html"

    def get_context(self, name: str, value: Any, attrs: dict[str, Any]) -> Context:
        attrs.setdefault("class", "vForeignKeyRawIdAdminField")

        context = super().get_context(name, value, attrs)
        app_name = self.rel.model._meta.app_label  # noqa: SLF001 Private member accessed
        model_name = self.rel.model._meta.object_name.lower()  # noqa: SLF001 Private member accessed

        context.update(
            name=name,
            app_name=app_name,
            model_name=model_name,
            related_url=reverse(
                f"admin:{app_name}_{model_name}_changelist",
                current_app=self.admin_site.name,
            ),
            url=f"?{urlencode(self.url_parameters())}",
        )
        return context

    @property
    def media(self) -> forms.Media:
        return forms.Media(
            js=[
                "admin/js/vendor/jquery/jquery.min.js",
                "admin/js/jquery.init.js",
                "admin/js/core.js",
                "dynamic_raw_id/js/dynamic_raw_id.js",
            ]
        )


class DynamicRawIDMultiIdWidget(DynamicRawIDWidget):
    def get_context(self, name: str, value: Any, attrs: dict[str, Any]) -> Context:
        attrs.setdefault("class", "vManyToManyRawIdAdminField")
        value = ",".join([force_str(v) for v in value]) if value else ""
        return super().get_context(name, value, attrs)
