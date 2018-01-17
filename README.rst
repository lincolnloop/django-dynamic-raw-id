.. image:: https://travis-ci.org/lincolnloop/django-dynamic_rawid.svg?branch=master
    :target: https://travis-ci.org/lincolnloop/django-dynamic_rawid

.. image:: https://codecov.io/github/lincolnloop/django-dynamic_rawid/coverage.svg?branch=master
    :target: https://codecov.io/github/lincolnloop/django-dynamic_rawid?branch=master


.. important:: django-salmonella was renamed to django-dynamic-rawid and
   re-released as version 2.0. The latest django-salmonella version was 1.2.
   You can upgrade your code by simply replacing:

   - ``django-salmonella`` with ``django-dynamic-rawid``
   - ``salmonella`` with ``dynamic_rawid``.

====================
django-dynamic_rawid
====================

A Django admin raw_id_fields widget replacement that handles display of an
object's string value on change and can be overridden via a template.
See this example:

.. image:: http://d.pr/i/10GtM.png
    :target: http://d.pr/i/1kv7d.png

Installation
============

Install the package with ``pip``::

    $ pip install django-dynamic-rawid

Put ``dynamic_rawid`` to your list of ``INSTALLED_APPS``::

    INSTALLED_APPS = (
        # ... other apps
        'dynamic_rawid',
    )

And add the ``urlpattern``::

    urlpatterns = [
        # ...
        url(r'^admin/dynamic_rawid/', include('dynamic_rawid.urls')),
    ]

``dynamic_rawid`` comes with some static files so don't forget to run
``manage.py collectstatic``.

Usage
=====

To start using django-dynamic_rawid in your application all you need to do is
implement ``dynamic_rawidMixin`` in your  ``ModelAdmin`` class and add the desired
fields to a list of ``dynamic_rawid_fields``::

    from dynamic_rawid.admin import dynamic_rawidMixin

    class UserProfileAdmin(dynamic_rawidMixin, admin.ModelAdmin):
        dynamic_rawid_fields = ('user',)

You can use dynamic_rawid widgets in a Admin filter as well::

    from dynamic_rawid.admin import dynamic_rawidMixin
    from dynamic_rawid.filters import dynamic_rawidFilter

    class UserProfileAdmin(dynamic_rawidMixin, admin.ModelAdmin):
       list_filter = (
           ('dynamic_rawid_fk', dynamic_rawidFilter),
       )


Customizing the value of the dynamic widget
===========================================

The coolest feature of django-dynamic_rawid is the ability to customize the output
of the value displayed alongside the ``dynamic_rawidIdWidget``.  There is a basic
implementation if all you want is your object's ``__unicode__`` value. To change
the value displayed all you need to do is implement the correct template.

Django-dynamic_rawid looks for this template structure ``dynamic_rawid/<app>/<model>.html``
and ``dynamic_rawid/<app>/multi_<model>.html`` (for multi-value lookups).

For instance, if I have a blog post with a ``User`` dynamic_rawid field that I want
display as ``Firstname Lastname``, I would create the template
``dynamic_rawid/auth/user.html`` with::

    <span>{{ object.0.first_name }} {{ object.0.last_name }}</span>

A custom admin URL prefix
=========================

If you have your admin *and* the dynamic_rawid scripts located on a different
prefix than ``/admin/dynamic_rawid/`` you need adjust the ``dynamic_rawid_MOUNT_URL``
JS variable.

Example::

    # In case the script is setup at /foobar/dynamic_rawid/
    url(r'^foobar/dynamic_rawid/', include('dynamic_rawid.urls')),

    # Provide a
    <script>
        window.dynamic_rawid_MOUNT_URL = "{% url "admin:index" %}";
    </script>

An ideal place is the admin ``base_site.html`` template. Full example::

    {% extends "admin/base.html" %}

    {% block title %}{{ title }} | {{ site_title|default:_('Django site admin') }}{% endblock %}

    {% block extrahead %}
      {{ block.super }}
      <script>
        window.dynamic_rawid_MOUNT_URL = "{% url "admin:index" %}";
      </script>
    {% endblock %}

    {% block branding %}
    <h1 id="site-name"><a href="{% url 'admin:index' %}">{{ site_header|default:_('Django administration') }}</a></h1>
    {% endblock %}

    {% block nav-global %}{% endblock %}


Testing and Local Development
=============================

Run the testsuite in your local environment using::

    $ cd django-dynamic_rawid/
    $ pipenv install --dev
    $ pipenv run python ./runtests.py

Or use tox to test against various Django and Python versions::

    $ tox -r

You can also invoke the test suite or other 'manage.py' commands by calling
the ``django-admin`` tool with the test app settings::

    $ cd django-dynamic_rawid/
    $ pipenv install --dev
    $ pipenv run django-admin
    $ pipenv run django-admin test

This also allows you to run the internal testing app in a testserver, to
preview a sample of what django-dynamic_rawid is doing::

    $ pipenv run django-admin migrate
    $ pipenv run django-admin createsuperuser
    $ pipenv run django-admin runserver

.. note:: The default settings file is set in the ``.env`` file which
   pipenv automatically exposes::

    DJANGO_SETTINGS_MODULE=dynamic_rawid.tests.testapp.settings
