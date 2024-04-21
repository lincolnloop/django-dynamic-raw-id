from tempfile import TemporaryDirectory

DEBUG = True

SECRET_KEY = "super-secret-dynamic_raw_id-key"  # noqa: S105 Hardcoded password

DATABASES = {
    "default": {"ENGINE": "django.db.backends.sqlite3", "NAME": "testapp.db"},
}

DEFAULT_AUTO_FIELD = "django.db.models.AutoField"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ]
        },
    }
]

INSTALLED_APPS = [
    "django.contrib.contenttypes",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.sessions",
    "django.contrib.staticfiles",
    "django.contrib.messages",
    "dynamic_raw_id",
    "dynamic_raw_id.tests.testapp",
]

MIDDLEWARE = (
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
)


STATIC_ROOT = TemporaryDirectory().name
STATIC_URL = "/static/"
ROOT_URLCONF = "dynamic_raw_id.tests.testapp.urls"

STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]

TEST_SETTINGS = {
    "DEBUG": DEBUG,
    "SECRET_KEY": SECRET_KEY,
    "DATABASES": DATABASES,
    "TEMPLATES": TEMPLATES,
    "INSTALLED_APPS": INSTALLED_APPS,
    "MIDDLEWARE": MIDDLEWARE,
    "STATIC_ROOT": STATIC_ROOT,
    "STATIC_URL": STATIC_URL,
    "ROOT_URLCONF": ROOT_URLCONF,
    "STATICFILES_FINDERS": STATICFILES_FINDERS,
}
