from __future__ import annotations

from typing import TYPE_CHECKING, Any

from django import forms
from django.conf import settings
from django.contrib.admin import widgets
from django.core.exceptions import ImproperlyConfigured
from django.urls import reverse
from django.utils.encoding import force_str

if TYPE_CHECKING:
    from django.forms.renderers import BaseRenderer
    from django.template import Context


class DynamicRawIDImproperlyConfigured(ImproperlyConfigured):
    pass


class DynamicRawIDWidget(widgets.ForeignKeyRawIdWidget):
    template_name: str = "dynamic_raw_id/admin/widgets/dynamic_raw_id_field.html"

    def get_context(self, name: str, value: Any, attrs: dict[str, Any]) -> Context:
        context = super().get_context(name, value, attrs)
        model = self.rel.model
        app_label = model._meta.app_label  # noqa: SLF001 Private member accessed
        model_name = model._meta.object_name.lower()  # noqa: SLF001 Private member accessed
        related_url = reverse(
            f"admin:{app_label}_{model_name}_changelist",
            current_app=self.admin_site.name,
        )

        params = self.url_parameters()
        url = "?" + "&".join([f"{k}={v}" for k, v in params.items()]) if params else ""
        if "class" not in attrs:
            attrs["class"] = (
                "vForeignKeyRawIdAdminField"  # The JavaScript looks for this hook.
            )
        app_name = model._meta.app_label.strip()  # noqa: SLF001 Private member accessed
        model_name = model._meta.object_name.lower().strip()  # noqa: SLF001 Private member accessed

        context.update(
            {
                "name": name,
                "app_name": app_name,
                "model_name": model_name,
                "related_url": related_url,
                "url": url,
            }
        )
        return context

    @property
    def media(self) -> forms.Media:
        extra = "" if settings.DEBUG else ".min"
        return forms.Media(
            js=[
                f"admin/js/vendor/jquery/jquery{extra}.js",
                "admin/js/jquery.init.js",
                "admin/js/core.js",
                "dynamic_raw_id/js/dynamic_raw_id.js",
            ]
        )


class DynamicRawIDMultiIdWidget(DynamicRawIDWidget):
    def value_from_datadict(
        self,
        data: dict[str, Any],
        files: Any | None,
        name: str,
    ) -> str | None:
        value = data.get(name)
        if value:
            return value.split(",")
        return None

    def render(
        self,
        name: str,
        value: Any,
        attrs: dict[str, Any] | None = None,
        renderer: BaseRenderer | None = None,
    ) -> str:
        attrs["class"] = "vManyToManyRawIdAdminField"
        value = ",".join([force_str(v) for v in value]) if value else ""
        return super().render(name, value, attrs, renderer=renderer)
