from stream_framework.activity import Activity
from stream_framework.verbs.base import Add
from benchmark.feeds import UserFeed, TimelineFeed
from cassandra.cqlengine.management import sync_table


'''
Issues:

* How do we point the worker instances to Cassandra and RabbitMQ?
* Cloudformation and instance configuration look like quite a bit of work
* Creating a new backend for Stream-Framework is not as easy as it should be

'''

def create_activity():
    activity = Activity(
        13,
        Add,
        42,
    )
    return activity


if __name__ == '__main__':
    for feed_class in [UserFeed, TimelineFeed]:
        timeline = feed_class.get_timeline_storage()
        sync_table(timeline.model)
    activity = create_activity()
    feed = UserFeed(13)
    for x in range(100):
        print activity, feed.add(activity)