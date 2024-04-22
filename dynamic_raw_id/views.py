from __future__ import annotations

from typing import TYPE_CHECKING, Any

from django.apps import apps
from django.db.models.base import ModelBase
from django.http import (
    HttpRequest,
    HttpResponse,
    HttpResponseBadRequest,
    HttpResponseForbidden,
    HttpResponseNotFound,
)
from django.urls import reverse
from django.views.generic import TemplateView

if TYPE_CHECKING:
    from django.template import Context


class LabelView(TemplateView):
    app_name: str
    model_name: str
    model: ModelBase
    template_name = "dynamic_raw_id/label.html"
    template_object_name: str = "object"

    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        self.app_name = kwargs["app_name"]
        self.model_name = kwargs["model_name"]

        # User must be authorized and at least staff level.
        # Intentionally raising a NotFound here to not indicate this is an API response.
        if not request.user.is_authenticated or not request.user.is_staff:
            return HttpResponseNotFound()

        # User must have 'view' permission of the given app_name/model_name.
        if not request.user.has_perm(f"{self.app_name}.view_{self.model_name}"):
            return HttpResponseForbidden()

        # The list of to obtained objects is in GET.id.
        # No need to resume if we didn't get it.
        if "id" not in request.GET:
            msg = "No list of objects given"
            return HttpResponseBadRequest(msg)

        # Make sure, the given app_name/model_name exists.
        try:
            self.model = apps.get_model(self.app_name, self.model_name)
        except LookupError:
            return HttpResponseBadRequest()

        return super().dispatch(request, *args, **kwargs)

    def get_template_names(self) -> list[str]:
        return [
            f"dynamic_raw_id/{self.app_name}/{self.model_name}.html",
            self.template_name,
        ]

    def get_obj_context(self) -> tuple[str, Any] | None:
        try:
            obj = self.model.objects.get(pk=self.request.GET["id"])
        except (self.model.DoesNotExist, ValueError):
            return None

        return (
            str(obj),
            reverse(f"admin:{self.app_name}_{self.model_name}_change", args=[obj.pk]),
        )

    def get_context_data(self, **kwargs: Any) -> Context:
        context = super().get_context_data(**kwargs)
        context.update(**{self.template_object_name: self.get_obj_context()})
        return context


class MultiLabelView(LabelView):
    """
    Same as  LabelView, but accepts multiple GET.id values,
    given as a comma separated list.
    """

    multi: bool = False
    template_name = "dynamic_raw_id/multi_label.html"
    template_object_name: str = "objects"

    def get_obj_context(self) -> list[tuple[str, Any]] | None:
        try:
            object_id_list = self.model.objects.filter(
                pk__in=self.request.GET["id"].split(",")
            )
        except ValueError:
            return None

        objects = self.model.objects.filter(pk__in=object_id_list)
        return [
            (
                str(obj),
                reverse(
                    f"admin:{self.app_name}_{self.model_name}_change", args=[obj.pk]
                ),
            )
            for obj in objects
        ]

    def get_template_names(self) -> list[str]:
        return [
            f"dynamic_raw_id/{self.app_name}/multi_{self.model_name}.html",
            self.template_name,
        ]
