import os

app_name = os.getenv('APPLICATION_NAME', 'hope')


LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'root': {
        'level': 'DEBUG',
        'handlers': ['sentry', 'syslog'],
    },
    'formatters': {
        'verbose': {
            'format': u'{}: %(levelname)s %(name)s %(module)s '
                      u'%(lineno)d: %(message)s'.format(app_name)
        },
        'default': {
            'format': u'%(message)s'
        }
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'sentry': {
            'level': 'WARNING',
            'class': 'raven.contrib.django.raven_compat.handlers.SentryHandler',
        },
        'null': {
            'level': 'DEBUG',
            'class': 'logging.NullHandler',
        },
        'syslog': {
            'level': 'DEBUG',
            'class': 'logging.handlers.SysLogHandler',
            'address': '/dev/log',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['null'],
            'level': 'INFO',
            'propagate': True,
        },
        'raven': {
            'level': 'DEBUG',
            'handlers': ['syslog'],
            'propagate': False,
        },
        'sentry.errors': {
            'level': 'DEBUG',
            'handlers': ['syslog'],
            'propagate': False,
        },
    }
}
