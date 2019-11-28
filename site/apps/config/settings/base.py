'''
Common settings and globals.

See:
    - https://docs.djangoproject.com/en/dev/topics/settings/
    - https://docs.djangoproject.com/en/dev/ref/settings/
'''
import re

import environ


# -------------------------------------
# GENERAL SETUP
# -------------------------------------

# Paths
# =====================================
# Paths here the `environ.Path` which provides a special api around os paths.
#
# How to use:
#
#   # Get the path as a string
#   PROJECT_PATH()
#
#   # Get a sub-directory or file path as a string
#   # Note: This calls the path directly and not through .path
#   PROJECT_PATH('static')
#   PROJECT_PATH('foo.json')
#
#   # Get a path as an environ Path object
#   PROJECT_PATH.path('static')
#
# Docs:
#   - https://github.com/joke2k/django-environ

WORKING_PATH = environ.Path(__file__) - 1
BASE_PATH = WORKING_PATH - 3
PROJECT_PATH = BASE_PATH.path('apps')
LOG_DIR = BASE_PATH()


# Env
# =====================================

env = environ.Env()
environ.Env.read_env(BASE_PATH('.env'))

IS_PRODUCTION = not env.bool('IS_LOWER_ENVIRONMENT', False)


# -------------------------------------
# DJANGO CONFIGURATION
# -------------------------------------

WSGI_APPLICATION = 'apps.config.wsgi.application'
ROOT_URLCONF = 'apps.config.urls'
DEBUG = False if IS_PRODUCTION else env.bool('DEBUG', False)
ALLOWED_HOSTS = ('localhost', '127.0.0.1',)
SITE_ID = 1
SITE_NAME = env('SITE_NAME', default='example.com')

ADMINS = (('app admin'),)

MANAGERS = ADMINS

FIXTURE_DIRS = (PROJECT_PATH('fixtures'),)

INSTALLED_APPS = (
    # Overrides
    # Apps that must come first (may include local apps)
    'apps.utils',

    # Django apps
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    # 'django.contrib.sitemaps',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.redirects',
    'django.contrib.admin',
    # 'django.contrib.gis',
    # 'django.contrib.gis.geoip',

    # Local apps
    'apps.web',
    'apps.ui_kit',
    'apps.api',

    # Third-party Apps
    'django_extensions',
    'crispy_forms',
    'rest_framework',
    'rest_framework.authtoken',
    'adminsortable2',
    'solo',
    'optimized_image',
)

MIDDLEWARE = (
    'whitenoise.middleware.WhiteNoiseMiddleware',
    # Must come first

    # Default Django middleware.
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.contrib.redirects.middleware.RedirectFallbackMiddleware',
)

MESSAGE_STORAGE = 'django.contrib.messages.storage.session.SessionStorage'

# Databases
# =====================================

DATABASES = {
    # Raises ImproperlyConfigured exception if DATABASE_URL not in os.environ
    'default': env.db('DATABASE_URL', default='postgres://djangodb:djangodb@postgres/djangodb'),
}

# DATABASES['default']['ENGINE'] = 'django.contrib.gis.db.backends.postgis'


# Logging
# =====================================

LOG_LEVEL = env('LOG_LEVEL', default='ERROR')


# Templates
# =====================================

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': (
            PROJECT_PATH.path('overrides', 'templates').__str__(),
            'templates',
        ),
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': (
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.request',
                'apps.web.context_processors.add_variable_to_context',

                # Local
                'apps.utils.context_processors.global_variables',
                'apps.web.context_processors.web_settings',
            ),
        },
    }
]


# Storages
# =====================================

USE_HTTPS_FOR_ASSETS = env.bool('USE_HTTPS_FOR_ASSETS', False)
ASSET_VERSION = env('ASSET_VERSION', default=False)


# Staticfiles
# =====================================

STATIC_ROOT = BASE_PATH('collected-static')
STATIC_URL = '/static/'

# Add project/static to staticfile resolution
# Entries here are eligible for `collectstatic` as well
# See:
# https://docs.djangoproject.com/en/1.10/ref/contrib/staticfiles/#collectstatic
STATICFILES_DIRS = (
    BASE_PATH('static'),
    BASE_PATH('apps/web/static'),
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)
SERVE_STATIC = False

MEDIA_ROOT = PROJECT_PATH('uploads')
MEDIA_URL = '/uploads/'

# Options for django-optimized-image
# https://github.com/dchukhin/django_optimized_image
OPTIMIZED_IMAGE_METHOD = 'pillow'
OPTIMIZED_IMAGE_IGNORE_EXTENSIONS = ['gif']


# Locale / I18N & L10N
# =====================================

# Set to True to automatically enable django's i81n
# Note: This is a custom (i.e., non-native Django setting) but is used to
#       branch in a few places to enable Django's I18N and L10N automatically.
AUTO_ENABLE_I18N = False  # noqa

TIME_ZONE = 'America/Los_Angeles'
USE_TZ = True

USE_I18N = AUTO_ENABLE_I18N
USE_L10N = AUTO_ENABLE_I18N

LANGUAGE_CODE = 'en'
LANGUAGES = (
    ('en', 'English'),
    # Add additional / change languages here
    # ('de', 'German'),
    # ('es', 'Spanish'),
)

LOCALE_PATHS = (
    PROJECT_PATH('apps/web/locale'),
)


# Cache
# =====================================

CACHE_TIMEOUT = env('CACHE_TIMEOUT', default=60 * 60)
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'TIMEOUT': CACHE_TIMEOUT,
    }
}


# -------------------------------------
# VENDOR CONFIGURATION
# -------------------------------------


# Redis
# =====================================

REDIS_HOST = env('REDIS_HOST', default='redis://localhost:6379')

  # noqa

# UploadCare
# Leaving here so support legacy code
# =====================================

UPLOADCARE = {
    'pub_key': env('UPLOADCARE_PUB_KEY', default=''),
    'secret': env('UPLOADCARE_SECRET_KEY', default=''),
}

  # noqa

# Redactor
# =====================================


# Thumbnails
# =====================================

THUMBNAIL_PROCESSORS = (
    'easy_thumbnails.processors.colorspace',
    'easy_thumbnails.processors.autocrop',
    'filer.thumbnail_processors.scale_and_crop_with_subject_location',
    'easy_thumbnails.processors.filters'
)

# Taggit / Taggit Autosuggest
# =====================================

TAGGIT_AUTOSUGGEST_CSS_FILENAME = 'taggit-autosuggest.css'
TAGGIT_AUTOSUGGEST_STATIC_BASE_URL = re.sub('/$', '', STATIC_URL)


# Slack
# =====================================

# SLACK_INCOMING_WEB_HOOK = env('SLACK_INCOMING_WEB_HOOK', default=None)
# SLACK_CHANNEL = env('SLACK_CHANNEL', default='mission-logs')
# SLACK_USER_NAME = 'Logger:{0}'.format(
#     env('SLACK_USER_NAME', default='PROD' if IS_PRODUCTION else 'UNSET'),
# )


# Crispy Forms
# =====================================

CRISPY_TEMPLATE_PACK = 'bootstrap3'


# Rest Framework
# =====================================

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    )
}


# -------------------------------------
# PROJECT SETTINGS
# -------------------------------------

# Analytics
# =====================================

GTM_CODE = env('GTM_CODE', default='')
OPTIMIZELY_ID = env('OPTIMIZELY_ID', default='')


# Misc
# =====================================

GOOGLE_API_KEY = env('GOOGLE_API_KEY', default='')
LIVECHAT_LICENSE = env('LIVECHAT_LICENSE', default='')


# -------------------------------------
# SPRINKLR CONFIGURATION
# -------------------------------------

SPRINKLR_HOST = env('SPRINKLR_HOST', default='')
SPRINKLR_SITE_ID = env('SPRINKLR_SITE_ID', default='')
SPRINKLR_USER_ID = env('SPRINKLR_USER_ID', default='')
SPRINKLR_SECRET_KEY = env('SPRINKLR_SECRET_KEY', default='')
SPRINKLR_JWT = env('SPRINKLR_JWT', default='')

# -------------------------------------
# FACEBOOK CONFIGURATION
# -------------------------------------

FACEBOOK_APP_ID = env('FACEBOOK_APP_ID', default='')


# -------------------------------------
# HSTS
# -------------------------------------
# NOTE: This was breaking staging
# SECURE_HSTS_SECONDS = 63072000
# SECURE_HSTS_INCLUDE_SUBDOMAINS = True
# SECURE_HSTS_PRELOAD = True
# SECURE_SSL_REDIRECT = True
