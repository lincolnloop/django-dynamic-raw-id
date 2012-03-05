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
    
    
Finally
*******

Add ``salmonella`` to your project's ``INSTALLED_APPS`` and you should be ready to go::

    INSTALLED_APPS = (
        ...
        'salmonella',
        ...
    )

.. _github.com: http://github.com/lincolnloop/django-salmonella