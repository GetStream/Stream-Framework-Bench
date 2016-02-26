
SECRET_KEY = '123456789'

STREAM_DEFAULT_KEYSPACE = 'stream_framework_bench'

# configure the cassandra hosts
STREAM_CASSANDRA_HOSTS = [
    '127.0.0.1'
]
# configure the broker url
BROKER_URL = 'amqp://guest:guest@localhost:5672//'


CELERY_EAGER_PROPAGATES_EXCEPTIONS = True
DEBUG = True

STREAM_METRIC_CLASS = 'benchmark.metrics.BenchMetrics'
STREAM_METRICS_OPTIONS = {
    'host': 'localhost',
    'port': 8125,
    'prefix': 'stream'
}

INSTALLED_APPS = [
    'benchmark'
]

# we need to fake this, required by celery + django lib
# urls.py is empty
ROOT_URLCONF = 'benchmark.urls'

import os
environment = os.environ.get('ENVIRONMENT')

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        '': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': True
        },
        'bench': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False
        },
    }
}
# TODO: somehow Django isn't picking this up automatically (it should)
# as a workaround we're calling dictConfig directly
from logging.config import dictConfig
dictConfig(LOGGING)

# production settings
if environment == 'production':
    DEBUG = False
    CELERY_ALWAYS_EAGER = False
    
if environment == 'rabbit':
    CELERY_ALWAYS_EAGER = False