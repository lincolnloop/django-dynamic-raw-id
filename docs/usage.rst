Usage
=====

To start using django-salmonella in your application all you need to do is implement ``SalmonellaMixin`` in your  ``ModelAdmin`` class::

    from salmonella.admin import SalmonellaMixin

    class UserProfileAdmin(SalmonellaMixin, admin.ModelAdmin):
        salmonella_fields = ('user',)

Note
****

Don't forget to enable model admin's for each field specified in salmonella_fields.

Customizing the value of the dynamic widget
*******************************************

The coolest feature of django-salmonella is the ability to customize the output of the value displayed alongside the ``SalmonellaIdWidget``.  There is a
basic implementation if all you want is your object's ``__unicode__`` value.  To change the value displayed all you need to do is implement the correct
template.  Django-salmonella looks for this template structure ``salmonella/<app>/<model>.html`` and ``salmonella/<app>/multi_<model>.html`` (for multi-value lookups).

For instance, if I have a blog post with a ``User`` salmonella field that I want display as ``Firstname Lastname``, I would create the template ``salmonella/auth/user.html`` with::

    <span>{{ object.0.first_name }} {{ object.0.last_name }}</span>