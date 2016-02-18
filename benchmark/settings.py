
SECRET_KEY = '123456789'

STREAM_DEFAULT_KEYSPACE = 'stream_framework'

STREAM_CASSANDRA_HOSTS = [
    '127.0.0.1'
]

CELERY_ALWAYS_EAGER = True

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        # Send all messages to console
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        '': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
        'bench': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
    },
}
DEBUG = True

