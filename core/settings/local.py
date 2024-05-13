from .base import *

DEBUG = env.bool('DJANGO_DEBUG', default=True)
ALLOWED_HOSTS = env.list('DJANGO_ALLOWED_HOSTS', default=['*'])

ALLOW_DEBUG_TOOLBAR = DEBUG and env.bool('DJANGO_ALLOW_DEBUG_TOOLBAR', default=True)
ALLOW_SQL_QUERY_LOGGING = DEBUG and env.bool('DJANGO_ALLOW_SQL_QUERY_LOGGING', default=True)

if ALLOW_DEBUG_TOOLBAR:
    INTERNAL_IPS = env.list('DJANGO_INTERNAL_IPS', default=['127.0.0.1'])

    INSTALLED_APPS += [
        # Libs
        'debug_toolbar',
    ]

    MIDDLEWARE += [
        'debug_toolbar.middleware.DebugToolbarMiddleware',
    ]

if ALLOW_SQL_QUERY_LOGGING:
    LOGGING = {
        'version': 1,
        'filters': {
            'require_debug_true': {
                '()': 'django.utils.log.RequireDebugTrue',
            }
        },
        'handlers': {
            'console': {
                'level': 'DEBUG',
                'filters': ['require_debug_true'],
                'class': 'logging.StreamHandler',
            }
        },
        'loggers': {
            'django.db.backends': {
                'level': 'DEBUG',
                'handlers': ['console'],
                'propagate': False,
            }
        }
    }
