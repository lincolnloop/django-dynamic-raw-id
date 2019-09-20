=========
Changelog
=========

v2.7 (2019-09-19)
=======================
- Django 3.0alpha compatibility
- Replace `render_to_response` with `render`
- Replace `django.utils.six` with `six`
- Remove unneeded "dunder" methods from test settings in `runtests.py`
- Replace `staticfiles` and `admin_static`

v2.6 (2019-06-21)
=================

- BACKWARDS INCOMPATIBLE: Dropped support for Django <1.11.
- BACKWARDS INCOMPATIBLE: Dropped support for Python 3.4.
- Django 2.2 compatibility and tests.
- General code cleanup.
- Pipenv support for local development.
- Some visual fixes around icons and alignment.

v2.5 (2018-12-09)
=================

- Django 2.1 compatibility and tests.

v2.4 (2018-04-09)
=================

- Fixes missing icons in Admin views.
- Fixes missing JS handling when using a custom /admin/ url.

v2.3 (2018-01-18)
=================

- BACKWARDS INCOMPATIBLE: Renamed the project to `django-dynamic-raw-id`.
  to reflect what it's  actually doing.
- Fixed glass lookup icon in Django 1.10 and below.
- Specific ordering of media asset loading.

v1.2 (2018-01-17)
=================

- Multiple fixes and enhancements.
- Full Selenium based testsuite.
- Django 2.0 and Python 3 compatibility.
- pipenv support.
