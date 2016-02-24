
SECRET_KEY = '123456789'

STREAM_DEFAULT_KEYSPACE = 'stream_framework_bench'

# configure the cassandra hosts
STREAM_CASSANDRA_HOSTS = [
    '127.0.0.1'
]
# configure the broker url
BROKER_URL = 'amqp://guest:guest@localhost:5672//'

CELERY_ALWAYS_EAGER = True
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

# production settings
if environment == 'production':
    DEBUG = False
    CELERY_ALWAYS_EAGER = False