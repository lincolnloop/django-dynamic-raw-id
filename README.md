django-salmonella
=================

A raw_id_fields widget replacement that handles display of an object's string value on change and can be overridden via a template.

Installation
------------

	$ pip install salmonella

Usage
-----

Include the file in your settings.py:

	INSTALLED_APPS = (
		...
		'salmonella',
		...
	)

Collect the static file:

	$ manage.py collectstatic

Configure your model admin, here is an example:

	from salmonella import SalmonellaModelAdmin

	class UserProfileAdmin(SalmonellaModelAdmin):
	    salmonella_fields = ('user',)
