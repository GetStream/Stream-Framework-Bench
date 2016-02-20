from stream_framework.feeds.cassandra import CassandraFeed


class UserFeed(CassandraFeed):
    key_format = 'feed:user:%(user_id)s'


class TimelineFeed(CassandraFeed):
    key_format = 'feed:timeline:%(user_id)s'
