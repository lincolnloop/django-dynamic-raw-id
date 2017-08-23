#!/usr/bin/env python
from setuptools import find_packages, setup

setup(
    name='django-salmonella',
    version='1.1',
    author='Lincoln Loop: Seth Buntin, Yann Malet',
    author_email='info@lincolnloop.com',
    description=("raw_id_fields widget replacement that handles display of an object's "
                 "string value on change and can be overridden via a template."),
    long_description=open('README.rst').read(),
    url='https://github.com/lincolnloop/django-salmonella/',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Framework :: Django',
    ],
    packages=find_packages(),
    package_data={
        'salmonella': ['templates/*.*', 'static/*.*'],
        'docs': ['*'],
    },
    include_package_data=True,
    install_requires=[
        'django>=1.8',
    ],
)
