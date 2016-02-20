
SECRET_KEY = '123456789'

STREAM_DEFAULT_KEYSPACE = 'stream_framework_bench'

# configure the cassandra hosts
STREAM_CASSANDRA_HOSTS = [
    '127.0.0.1'
]
# configure the broker url
BROKER_URL = 'amqp://guest:guest@localhost:5672//'

CELERY_ALWAYS_EAGER = True
DEBUG = True
