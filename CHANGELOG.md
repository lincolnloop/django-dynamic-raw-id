# Changelog

## v4.2 (2024-06-18)

- Fix Multi Widgets which was showing multiple commas after save. #103

## v4.1 (2024-05-20)

- Overall code cleanup.
- Refactored tests. Now full test coverage.

## v4.0 (2024-04-21)

- Django 4.2 compatibility and tests.
- Django 5.0 compatibility and tests.
- Requires Python 3.8 or up.
- Switch package management to Poetry.

## v3.0 (2022-03-20)

- Django 4.0 compatibility and tests.
- Requires Django 3.2 or up.
- Requires Python 3.7 or up.
- _Note:_ You may now need to change the order and put the dynamic-raw-id
  include before the generic admin include. See Readme for details.

## v2.8 (2020-12-02)

- Django 3.1 compatibility and tests.

## v2.7 (2020-05-02)

- Django 3.0 compatibility and tests.

## v2.6 (2019-06-21)

- BACKWARDS INCOMPATIBLE: Dropped support for Django <1.11.
- BACKWARDS INCOMPATIBLE: Dropped support for Python 3.4.
- Django 2.2 compatibility and tests.
- General code cleanup.
- Pipenv support for local development.
- Some visual fixes around icons and alignment.

## v2.5 (2018-12-09)

- Django 2.1 compatibility and tests.

## v2.4 (2018-04-09)

- Fixes missing icons in Admin views.
- Fixes missing JS handling when using a custom /admin/ url.

## v2.3 (2018-01-18)

- BACKWARDS INCOMPATIBLE: Renamed the project to `django-dynamic-raw-id`.
  to reflect what it's actually doing.
- Fixed glass lookup icon in Django 1.10 and below.
- Specific ordering of media asset loading.

## v1.2 (2018-01-17)

- Multiple fixes and enhancements.
- Full Selenium based testsuite.
- Django 2.0 and Python 3 compatibility.
- pipenv support.
