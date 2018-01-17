DEBUG = True

SECRET_KEY = "super-secret-dynamic_rawid-key"

DATABASES = {
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
}

TEMPLATES = [
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
]

INSTALLED_APPS = [
    'dynamic_rawid',
    'dynamic_rawid.tests.testapp',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.sessions',
    'django.contrib.staticfiles',
    'django.contrib.contenttypes',
]

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

MIDDLEWARE = MIDDLEWARE_CLASSES

STATIC_ROOT = '/tmp/dynamic_rawid_static/'
STATIC_URL = '/static/'
ROOT_URLCONF = 'dynamic_rawid.tests.testapp.urls'
