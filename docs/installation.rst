Installation
============

You can install django-salmonella like many other Python libraries.

PyPi release
************

pip will install the library from the Python Package Index::

    $ pip install django-salmonella

or you can use Easy Install::

    $ easy_install django-salmonella

pip from source
***************

You can also install with pip straight from the `github.com`_ repository::

    $ pip install git+http://github.com/lincolnloop/django-salmonella.git#egg=django-salmonella

Add URLS
********

Add the following line to urls.py::

    urlpatterns = patterns('',
        ...
        (r'^admin/salmonella/', include('salmonella.urls')),
        ...
    )

Finally
*******

Add ``salmonella`` to your project's ``INSTALLED_APPS`` and you should be ready to go::

    INSTALLED_APPS = (
        ...
        'salmonella',
        ...
    )

Run manage.py collectstatic (Django 1.3+) or make sure the static files are available at STATIC_URL/salmonella/


.. _github.com: http://github.com/lincolnloop/django-salmonella