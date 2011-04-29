from setuptools import setup, find_packages

setup(
    name="django-salmonella",
    version="0.4.0",
    author='Lincoln Loop',
    author_email='info@lincolnloop.com',
    description=("raw_id_fields widget replacement that handles display of an object's "
                 "string value on change and can be overridden via a template."),
    packages=find_packages(),
    package_data={'salmonella': ['static/*.js', 'templates/salmonella/*.html']},
    url="http://github.com/lincolnloop/django-salmonella/",
    install_requires=['setuptools'],
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
