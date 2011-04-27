from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.db.models import get_model
from django.contrib.auth.decorators import user_passes_test

@user_passes_test(lambda u: u.is_staff)
def label(request, app_name, model_name, template_name="", multi=False,
          template_object_name="object"):
    object_id = request.GET.get("id", "")
    model_class = get_model(app_name, model_name)
    try:
        if multi:
            if object_id:
                object_id = object_id.split(",")
            lookup_param = "id__in"
            model_template = "salmanella/%s/multi_%s.html" % (app_name, model_name)
        else:
            model_template = "salmanella/%s/%s.html" % (app_name, model_name)
            lookup_param = "id"
        obj = model_class.objects.get(**{lookup_param: object_id})
    except model_class.DoesNotExist:
        return HttpResponse("")
    return render_to_response((model_template, template_name),
                                  {template_object_name: obj})