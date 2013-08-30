#!/usr/bin/env python
from setuptools import setup, find_packages

setup(
    name="django-salmonella",
    version='0.6.1',
    author='Lincoln Loop: Seth Buntin, Yann Malet',
    author_email='info@lincolnloop.com',
    description=("raw_id_fields widget replacement that handles display of an object's "
                 "string value on change and can be overridden via a template."),
    packages=find_packages(),
    package_data={'salmonella': [
        'static/salmonella/js/*.js',
        'static/salmonella/img/*.gif',
        'templates/salmonella/*.html',
        'templates/salmonella/admin/*.html',
        'templates/salmonella/admin/widgets/*.html'
    ]},
    include_package_data=True,
    url="http://github.com/lincolnloop/django-salmonella/",
    zip_safe=False,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
