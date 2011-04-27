from setuptools import setup, find_packages

README_FILE = open('README')
try:
    LONG_DESCRIPTION = README_FILE.read()
finally:
    README_FILE.close()

setup(
    name="django-salmonella",
    version="0.1.0",
    author='Lincoln Loop',
    author_email='info@lincolnloop.com',
    description=("raw_id_fields widget replacement that handles display of an object's "
                 "string value on change and can be overridden via a template."),
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    url="http://github.com/lincolnloop/salmonella/",
    install_requires=['setuptools'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
