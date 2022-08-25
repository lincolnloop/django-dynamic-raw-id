from django.apps import apps
from django.conf import settings
from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponseBadRequest, HttpResponseForbidden
from django.shortcuts import render
from django.urls import reverse
from django.urls.exceptions import NoReverseMatch


def dynamic_label_view(
    admin_site='admin'
):
    @user_passes_test(lambda u: u.is_staff)
    def label_view(
        request,
        app_name,
        model_name,
        template_name='',
        multi=False,
        template_object_name='object',
    ):
        object_list = []
        for pk in request.GET['id'].split(','):
            object_list.append(pk.strip())

        try:
            model = apps.get_model(app_name, model_name)
        except LookupError:
            msg = 'Model {0}.{1} does not exist.'.format(app_name, model_name)
            return HttpResponseBadRequest(settings.DEBUG and msg or '')

        else:
            if not request.user.has_perm('{0}.change_{1}'.format(app_name, model_name)):
                return HttpResponseForbidden()

        return get_change_view(
            request=request,
            app_name=app_name,
            model_name=model_name,
            model=model,
            object_list=object_list,
            admin_site=admin_site,
            template_name=template_name,
            multi=multi,
            template_object_name=template_object_name,
        )

    return label_view


def get_change_view(
    request,
    app_name,
    model_name,
    model,
    object_list,
    admin_site,
    template_name,
    multi,
    template_object_name,
):
    try:
        if multi:
            model_template = 'dynamic_raw_id/{0}/multi_{1}.html'.format(
                app_name,
                model_name,
            )
            objs = model.objects.filter(pk__in=object_list)
            objects = []
            for obj in objs:
                change_url = reverse(
                    '{0}:{1}_{2}_change'.format(
                        admin_site,
                        app_name,
                        model_name
                    ), args=[obj.pk]
                )
                obj = (obj, change_url)
                objects.append(obj)
            extra_context = {template_object_name: objects}
        else:
            model_template = 'dynamic_raw_id/{0}/{1}.html'.format(
                app_name,
                model_name,
            )
            obj = model.objects.get(pk=object_list[0])
            change_url = reverse(
                '{0}:{1}_{2}_change'.format(
                    admin_site,
                    app_name,
                    model_name
                ), args=[obj.pk]
            )
            extra_context = {template_object_name: (obj, change_url)}
    except ValueError:
        msg = 'ValueError during lookup'
        return HttpResponseBadRequest(settings.DEBUG and msg or '')
    except model.DoesNotExist:
        msg = 'Model instance does not exist'
        return HttpResponseBadRequest(settings.DEBUG and msg or '')
    except NoReverseMatch as e:
        if admin_site != 'admin':
            return get_change_view(
                request=request,
                app_name=app_name,
                model_name=model_name,
                model=model,
                object_list=object_list,
                admin_site='admin',
                template_name=template_name,
                multi=multi,
                template_object_name=template_object_name,
            )
        raise e

    return render(request, (model_template, template_name), extra_context)
