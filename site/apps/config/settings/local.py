'''Development settings and globals.'''

from .base import *  # noqa F402
import os

# -------------------------------------
# DJANGO CONFIGURATION
# -------------------------------------

# Django Setup
# =====================================

ALLOWED_HOSTS += ('docker.local', '.ngrok.io',)  # noqa F405
SECRET_KEY = env('SECRET_KEY', default='abcdefghijklmnopqrstuvwxyz')  # noqa F405

INSTALLED_APPS += (  # noqa F405
    'debug_toolbar',
    'storages',
)

MIDDLEWARE += (  # noqa F405
    'debug_toolbar.middleware.DebugToolbarMiddleware',
)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(name)s %(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(asctime)s %(message)s'
        },
    },
    'handlers': {
        'stream': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
        'applogfile': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(LOG_DIR, 'mission.log'),
            'maxBytes': 1024 * 1024 * 15,  # 15MB
            'backupCount': 10,
            'formatter': 'verbose'
        },
    },
    'loggers': {
        '': {
            'handlers': ['stream', ],
            'level': LOG_LEVEL,  # noqa F405
            # 'propagate': False,
        },
        'django.db': {
            'handlers': ['stream', ],
            'level': LOG_LEVEL,  # noqa F405
            # 'propagate': False,
        },
        'z.pool': {
            'handlers': ['stream', ],
            'level': LOG_LEVEL,  # noqa F405
            # 'propagate': False,
        },
        'django': {
            'handlers': ['stream', ],
            'level': LOG_LEVEL,  # noqa F405
            # 'propagate': False,
        },
        'mission': {
            'handlers': ['applogfile',],
            'level': 'DEBUG',
        },
    }
}

INTERNAL_IPS = ('127.0.0.1',)


def show_toolbar(request):
    return True


DEBUG_TOOLBAR_CONFIG = {
    'SHOW_TOOLBAR_CALLBACK': show_toolbar,
}


MEDIA_URL = env('REMOTE_MEDIA_URL', default='/uploads/')  # noqa F405

# -------------------------------------
# VENDOR CONFIGURATION
# -------------------------------------


# -------------------------------------
# HSTS
# -------------------------------------
# NOTE: This was breaking staging
# SECURE_SSL_REDIRECT = False
