django-salmonella
=================

A raw_id_fields widget replacement that handles display of an object's string value on change and can be overridden via a template.

Installation
------------

    $ pip install django-salmonella

Usage
-----

Include this app in your settings.py:

    INSTALLED_APPS = (
            ...
            'salmonella',
            ...
    )

Add its url to you urls.py:

    urlpatterns = patterns('',
        ...
        url(r'^admin/salmonella/', include('salmonella.urls')),
        ...
    )

Collect the static file:

    $ manage.py collectstatic

Configure your model admin, here is an example:

    from salmonella import SalmonellaMixin

    class UserProfileAdmin(SalmonellaMixin, admin.ModelAdmin):
        salmonella_fields = ('user',)

**Note** Don't forget to enable model admin's for each field specified in `salmonella_fields`.
