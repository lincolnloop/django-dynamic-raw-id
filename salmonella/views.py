from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.db.models import get_model
from django.contrib.auth.decorators import user_passes_test

@user_passes_test(lambda u: u.is_staff)
def label_view(request, app_name, model_name, template_name="", multi=False,
               template_object_name="object"):
    
    try:
        object_id = request.GET.get("id", "")
        model = get_model(app_name, model_name)
        if multi:
            if object_id:
                object_id = object_id.split(",")
            model_template = "salmonella/%s/multi_%s.html" % (app_name, model_name)
            obj = model.objects.filter(id__in=object_id)
        else:
            model_template = "salmonella/%s/%s.html" % (app_name, model_name)
            obj = model.objects.get(id=object_id)
    except model.DoesNotExist:
        return HttpResponse("")
    return render_to_response((model_template, template_name),
                              {template_object_name: obj})