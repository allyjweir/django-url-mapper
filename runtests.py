from django.conf import settings
from django.core.management import call_command

settings.configure(

    DATABASES={
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
        }
    },
    INSTALLED_APPS=(
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.staticfiles',
        'django.contrib.sites',
        'urlmapper'
    ),
    STATIC_URL='/',
    MIDDLEWARE_CLASSES=(
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.common.CommonMiddleware',
    ),
    ROOT_URLCONF=('urlmapper.tests.urls'),
    SITE_ID=1,
    TEMPLATE_CONTEXT_PROCESSORS=(
        'django.contrib.auth.context_processors.auth',
        'django.core.context_processors.i18n',
        'django.core.context_processors.request',
    ),
    URLMAPPER_KEYS=[
        'test_1',
        'test_2',
        'test_3',
        'test_4',
        'test_5'
    ],
    URLMAPPER_FUNCTIONS={
        'test_1': lambda: 'test_1_success',
        'test_2': lambda request: 'test_2_success'
    },
)

call_command('test')
