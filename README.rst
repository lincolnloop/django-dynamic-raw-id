.. image:: https://travis-ci.org/lincolnloop/django-salmonella.svg?branch=master
    :target: https://travis-ci.org/lincolnloop/django-salmonella

.. image:: https://codecov.io/github/lincolnloop/django-salmonella/coverage.svg?branch=master
    :target: https://codecov.io/github/lincolnloop/django-salmonella?branch=master

=================
django-salmonella
=================

A Django admin raw_id_fields widget replacement that handles display of an
object's string value on change and can be overridden via a template.
See this example:

.. image:: http://d.pr/i/10GtM.png
    :target: http://d.pr/i/1kv7d.png

Installation
============

Install the package with ``pip``::

    $ pip install django-salmonella

Put ``salmonella`` to your list of ``INSTALLED_APPS``::

    INSTALLED_APPS = (
        # ... other apps
        'salmonella',
    )

And add the ``urlpattern``::

    urlpatterns = [
        # ...
        url(r'^admin/salmonella/', include('salmonella.urls')),
    ]

``salmonella`` comes with some static files so don't forget to run
``manage.py collectstatic``.

Usage
=====

To start using django-salmonella in your application all you need to do is
implement ``SalmonellaMixin`` in your  ``ModelAdmin`` class and add the desired
fields to a list of ``salmonella_fields``::

    from salmonella.admin import SalmonellaMixin

    class UserProfileAdmin(SalmonellaMixin, admin.ModelAdmin):
        salmonella_fields = ('user',)

You can use Salmonella widgets in a Admin filter as well::

    from salmonella.admin import SalmonellaMixin
    from salmonella.filters import SalmonellaFilter

    class UserProfileAdmin(SalmonellaMixin, admin.ModelAdmin):
       list_filter = (
           ('salmonella_fk', SalmonellaFilter),
       )


Customizing the value of the dynamic widget
===========================================

The coolest feature of django-salmonella is the ability to customize the output
of the value displayed alongside the ``SalmonellaIdWidget``.  There is a basic
implementation if all you want is your object's ``__unicode__`` value. To change
the value displayed all you need to do is implement the correct template.

Django-salmonella looks for this template structure ``salmonella/<app>/<model>.html``
and ``salmonella/<app>/multi_<model>.html`` (for multi-value lookups).

For instance, if I have a blog post with a ``User`` salmonella field that I want
display as ``Firstname Lastname``, I would create the template
``salmonella/auth/user.html`` with::

    <span>{{ object.0.first_name }} {{ object.0.last_name }}</span>
