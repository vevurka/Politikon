import os
import sys
import urlparse

from django.utils.translation import ugettext_lazy as _

from celery.schedules import crontab
from constance import config
from datetime import timedelta
from path import path


DJANGO_PROJECT_ROOT = path(__file__).abspath().dirname().dirname().dirname()

# Django settings for politikon project.

DEBUG = True

ADMINS = (
    ('Jakub Lipinski', ''),
    ('Tomasz Grynfelder', '')
)

MANAGERS = ADMINS

TIME_ZONE = 'Europe/Warsaw'
LANGUAGE_CODE = 'pl'

LOCALE_PATHS = [
    '/app/locale',
]

LANGUAGES = [
    ('pl', _('Polish')),
]

SITE_ID = 1
SITE_URL = 'https://www.politikon.org.pl/'

USE_I18N = True
USE_L10N = True
USE_TZ = False

ASSETS_MANIFEST = "file:"

REDIS_BASE_URL = os.environ.get('REDISTOGO_URL', 'redis://localhost:6379')
REDIS_PARAMS = urlparse.urlparse(REDIS_BASE_URL)

# Celery config

REDIS_HOST = REDIS_PARAMS.hostname
REDIS_PORT = REDIS_PARAMS.port
REDIS_DB = 0
REDIS_CONNECT_RETRY = False

BROKER_URL = REDIS_BASE_URL + "/0"
CELERY_RESULT_BACKEND = REDIS_BASE_URL + "/1"
BROKER_TRANSPORT_OPTIONS = {'visibility_timeout': 3600}

CELERY_SEND_EVENTS = True
CELERY_TASK_RESULT_EXPIRES = 10
CELERY_DISABLE_RATE_LIMITS = False
CELERY_IGNORE_RESULT = True
CELERYBEAT_SCHEDULER = "djcelery.schedulers.DatabaseScheduler"
CELERY_ACCEPT_CONTENT = ['json', 'application/x-python-serialize']

CONSTANCE_BACKEND = 'constance.backends.database.DatabaseBackend'
# CONSTANCE_DATABASE_CACHE_BACKEND = 'default' # prior to changes in
# django-constances

CONSTANCE_CONFIG = {
    'PUBLISH_DELAY_IN_MINUTES': (10.0, 'minutes of delay between action and \
                                 it\'s publication'),
    'STARTING_CASH': (1000.0, 'cash for start'),
    'SMALL_EVENT_IMAGE_WIDTH': (340, 'small event image width'),
    'SMALL_EVENT_IMAGE_HEIGHT': (250, 'small event image height'),
    'BIG_EVENT_IMAGE_WIDTH': (1250, 'big event image width'),
    'BIG_EVENT_IMAGE_HEIGHT': (510, 'big event image height'),
    'DAILY_TOPUP': (100, 'daily cash topup'),
    'ADMIN_TOPUP': (100, 'amount of cash in admin panel'),
    'REQUIRED_FRIENDS_THRESHOLD': (3, 'required number of registered friends'),
    'VOICES_TO_RESOLVE': (3, 'required number of voices to resolve event')
}

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/var/www/example.com/static/"
STATIC_ROOT = DJANGO_PROJECT_ROOT / 'static_build'

# URL prefix for static files.
# Example: "http://example.com/static/", "http://static.example.com/"
STATIC_URL = '/static/'

STATICFILES_DIRS = (
    DJANGO_PROJECT_ROOT / 'static',
)

ASSETS_ROOT = DJANGO_PROJECT_ROOT / 'static'

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    # 'django_assets.finders.AssetsFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = '@2@yw=u4h152#iscro&(4pcka%m1eydvw=_sne)@10f9+t^g9='

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    # 'django.template.loaders.eggs.Loader',
)

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(DJANGO_PROJECT_ROOT, 'templates'),
            DJANGO_PROJECT_ROOT
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                # Insert your TEMPLATE_CONTEXT_PROCESSORS here or use this
                # list if you haven't customized them:
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.core.context_processors.request',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.request',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                # social auth
                'social.apps.django_app.context_processors.backends',
                'social.apps.django_app.context_processors.login_redirect',
                # custom context processor
                'politikon.context_processors.politikon_settings'
            ],
        },
    },
]

AUTHENTICATION_BACKENDS = (
    'social.backends.twitter.TwitterOAuth',
    'social.backends.facebook.FacebookOAuth2',
    'django.contrib.auth.backends.ModelBackend',
)

AUTH_USER_MODEL = 'accounts.UserProfile'

LOGIN_REDIRECT_URL = '/'
URL_PATH = ''
SOCIAL_AUTH_STRATEGY = 'social.strategies.django_strategy.DjangoStrategy'
SOCIAL_AUTH_STORAGE = 'social.apps.django_app.default.models.DjangoStorage'
SOCIAL_AUTH_USERNAME_FORM_HTML = 'missing.html'

# set it False to allow redirect to main page after cancel facebook authentication. If this is True
# then raise AuthCanceled (HttpError 500) - social/apps/django_app/middleware.py line 50
RAISE_EXCEPTIONS = False

SOCIAL_AUTH_PIPELINE = (
    'social.pipeline.social_auth.social_details',
    'social.pipeline.social_auth.social_uid',
    'social.pipeline.social_auth.auth_allowed',
    'social.pipeline.social_auth.social_user',
    'social.pipeline.user.get_username',
    'social.pipeline.mail.mail_validation',
    'social.pipeline.user.create_user',
    'accounts.pipeline.save_profile',
    'social.pipeline.social_auth.associate_user',
    # 'social.pipeline.debug.debug',
    'social.pipeline.social_auth.load_extra_data',
    'social.pipeline.user.user_details',
    # 'social.pipeline.debug.debug'
)

SOCIAL_AUTH_FACEBOOK_PROFILE_EXTRA_PARAMS = {
  'fields': 'id, name, email, friends'
}


MIDDLEWARE_CLASSES = (
    # last visit
    'politikon.middleware.SetLastVisitMiddleware',
    # forcing one hostname on production
    'politikon.middleware.HostnameRedirectMiddleware',
    # forcing SSL using https://github.com/rdegges/django-sslify.
    # This need to be the first middleware
    'sslify.middleware.SSLifyMiddleware',
    # adding basic auth
    # 'politikon.middleware.BasicAuthMiddleware',

    # cause redirection to when raise social module exceptions
    'social.apps.django_app.middleware.SocialAuthExceptionMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

# needed by SSLify
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

ROOT_URLCONF = 'politikon.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'politikon.wsgi.application'

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',

    'django_assets',
    'social.apps.django_app.default',

    # 'oauth_tokens',
    # 'm2m_history',
    'taggit',
    # 'twitter_api',
    # https://github.com/matthewwithanm/django-imagekit for images resizing
    'imagekit',

    'constance',
    'constance.backends.database',
    'djcelery',
    'gunicorn',
    'rest_framework',
    'rest_framework.authtoken',
    'djoser',

    'grappelli',
    'django.contrib.admin',

    'accounts',
    'bladepolska',
    'events',
    'politikon'
)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'root': {
        'level': 'WARNING',
        'handlers': ['console'],
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'formatters': {
        'verbose': {
            'format': '[%(asctime)-12s] [%(levelname)s] %(message)s',
            'datefmt': '%b %d %H:%M:%S'
        },
        'simple': {
            'format': '%(message)s'
        },
    },
    'handlers': {
        'null': {
            'level': 'DEBUG',
            'class': 'logging.NullHandler',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'stream': sys.stderr,
            'formatter': 'verbose'
        },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            'filters': ['require_debug_false'],
            'include_html': True,
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins', 'console'],
            'level': 'ERROR',
            'propagate': True,
        },
        'django.db.backends': {
            'handlers': ['console'],
            'level': 'ERROR',
            'propagate': False,
        },
        'politikon': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
    }
}

JINJA2_GLOBALS = {
    'config': config
}

JINJA2_EXTENSIONS = [
    'webassets.ext.jinja2.AssetsExtension',
    'jinja2.ext.with_',
    'jinja2.ext.do',
    'jinja2.ext.i18n',
    'jinja2.ext.loopcontrols',
]

GRAPPELLI_ADMIN_TITLE = 'Politikon'
GRAPPELLI_AUTOCOMPLETE_LIMIT = 10
# GRAPPELLI_SWITCH_USER = True

import djcelery
djcelery.setup_loader()

if 'test' in sys.argv:
    try:
        from test import *
    except ImportError:
        pass

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
    ),
}
