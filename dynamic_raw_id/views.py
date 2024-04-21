from django.apps import apps
from django.conf import settings
from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponseBadRequest, HttpResponseForbidden
from django.shortcuts import render
from django.urls import reverse


@user_passes_test(lambda u: u.is_staff)
def label_view(
    request,
    app_name,
    model_name,
    template_name="",
    multi=False,
    template_object_name="object",
):
    # The list of to obtained objects is in GET.id. No need to resume if we
    # didnt get it.
    if not request.GET.get("id"):
        msg = "No list of objects given"
        return HttpResponseBadRequest(settings.DEBUG and msg or "")

    # Given objects are either an integer or a comma-separated list of
    # integers. Validate them and ignore invalid values. Also strip them
    # in case the user entered values by hand, such as '1, 2,3'.
    object_list = []
    for pk in request.GET["id"].split(","):
        object_list.append(pk.strip())

    # Make sure this model exists and the user has 'change' permission for it.
    # If he doesnt have this permission, Django would not display the
    # change_list in the popup and the user were never able to select objects.
    try:
        model = apps.get_model(app_name, model_name)
    except LookupError:
        msg = f"Model {app_name}.{model_name} does not exist."
        return HttpResponseBadRequest(settings.DEBUG and msg or "")

    # Check 'view' or 'change' permission depending to Django's version
    if not request.user.has_perm(f"{app_name}.view_{model_name}"):
        return HttpResponseForbidden()

    try:
        if multi:
            model_template = f"dynamic_raw_id/{app_name}/multi_{model_name}.html"
            objs = model.objects.filter(pk__in=object_list)
            objects = []
            for obj in objs:
                change_url = reverse(
                    f"admin:{app_name}_{model_name}_change", args=[obj.pk]
                )
                obj = (obj, change_url)
                objects.append(obj)
            extra_context = {template_object_name: objects}
        else:
            model_template = f"dynamic_raw_id/{app_name}/{model_name}.html"
            obj = model.objects.get(pk=object_list[0])
            change_url = reverse(f"admin:{app_name}_{model_name}_change", args=[obj.pk])
            extra_context = {template_object_name: (obj, change_url)}
    # most likely the pk wasn't convertable
    except ValueError:
        msg = "ValueError during lookup"
        return HttpResponseBadRequest(settings.DEBUG and msg or "")
    except model.DoesNotExist:
        msg = "Model instance does not exist"
        return HttpResponseBadRequest(settings.DEBUG and msg or "")

    return render(request, (model_template, template_name), extra_context)
