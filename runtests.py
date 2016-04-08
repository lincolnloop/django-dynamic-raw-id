#!/usr/bin/env python
import sys

from django.conf import settings

SETTINGS = {
    'DEBUG': True,
    'DATABASES': {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': 'dev.db',
        },
        # 'default': {
        #     'ENGINE': 'django.db.backends.mysql',
        #     'NAME': 'dpaste',
        #     'USER': 'root',
        #     'PASSWORD': '',
        # }
    },
    'TEMPLATES': [
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': [],
            'APP_DIRS': True,
            'OPTIONS': {
                'context_processors': [
                    'django.template.context_processors.debug',
                    'django.template.context_processors.request',
                    'django.contrib.auth.context_processors.auth',
                ],
            },
        },
    ],
    'INSTALLED_APPS': [
        'salmonella',
        'salmonella.tests.testapp',
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.sessions',
        'django.contrib.staticfiles',
        'django.contrib.contenttypes',
    ],
    'MIDDLEWARE_CLASSES': (
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.middleware.common.CommonMiddleware',
    ),
    'STATIC_ROOT': '/tmp/salmonella_static/',
    'STATIC_URL': '/static/',
    'ROOT_URLCONF': 'salmonella.tests.testapp.urls'
}

def runtests(*test_args):
    # Setup settings
    if not settings.configured:
        settings.configure(**SETTINGS)

    from django import setup
    from django.test.runner import DiscoverRunner as TestRunner
    
    setup()
    test_runner = TestRunner(verbosity=1)
    failures = test_runner.run_tests(['salmonella'])
    if failures:
        sys.exit(failures)

if __name__ == '__main__':
    runtests(*sys.argv[1:])
