import os
import sys
from stream_framework.verbs import register, get_verb_storage
sys.path.insert(0, os.path.dirname(__file__))
os.environ["DJANGO_SETTINGS_MODULE"] = "benchmark.settings"
from django.conf import settings
from stream_framework.activity import Activity
from stream_framework.verbs.base import Add
from benchmark.feeds import UserFeed, TimelineFeed
from cassandra.cqlengine.management import sync_table, create_keyspace
from benchmark.manager import manager
from benchmark import tasks

'''
Issues:

* How do we gradually increase load
* Where do we track stats....?
* How do we point the worker instances to Cassandra and RabbitMQ?
* Cloudformation and instance configuration look like quite a bit of work
* Creating a new backend for Stream-Framework is not as easy as it should be

Benchmark script

* Add activities (maybe wrap this in a task)
* Follow users
* Read activities (again maybe wrap this in a task)


'''







def create_activity(user_id):
    verbs = get_verb_storage()
    verb = verbs.values()[user_id % len(verbs)]
    activity = Activity(
        user_id,
        verb,
        42,
    )
    return activity

USERS = 100
FOLLOWERS_RANGE = (0, 2000)
ACTIVITIES_CREATION_RANGE = (0, 5)

if __name__ == '__main__':
    import boto3
    client = boto3.client('cloudformation')
    
    current_dir = os.path.dirname(__file__)
    cloudformation_dir = os.path.join(current_dir, 'cloudformation')
    cloudformation_files = []
    for (dirpath, dirnames, filenames) in os.walk(cloudformation_dir):
        cloudformation_files = [f for f in filenames if f.endswith('.json')]
        break
    
    for filename in cloudformation_files:
        print 'validating', filename
        file_path = os.path.join(cloudformation_dir, filename)
        template_body = open(file_path).read()
        client.validate_template(TemplateBody=template_body)
    
    1/0
    create_keyspace('stream_framework', 'SimpleStrategy', 3)
    for feed_class in [UserFeed, TimelineFeed]:
        timeline = feed_class.get_timeline_storage()
        sync_table(timeline.model)
    
    user_id = 13
    for user_id in range(USERS):
        for x in range(5):
            activity = create_activity(user_id)
            tasks.add_user_activity.delay(user_id, activity)
        manager.follow_user(user_id, 14)
        tasks.read_feed(user_id)
