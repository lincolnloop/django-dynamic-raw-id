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

Set up your urls.py:

	urlpatterns = patterns('',
		...
		(r'^salmonella/', include('salmonella.urls')),
		...
	)

Collect the static file:

	$ manage.py collectstatic

Configure your model admin, here is an example:

	from salmonella import SalmonellaModelAdmin

	class UserProfileAdmin(SalmonellaModelAdmin):
	    salmonella_fields = ('user',)

*NOTE:* This assumes you have already included the jQuery javascript library and it is available on the admin pages where Salmonella is being used.
