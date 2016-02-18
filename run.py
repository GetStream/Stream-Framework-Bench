import os
import sys
sys.path.insert(0, os.path.dirname(__file__))
os.environ["DJANGO_SETTINGS_MODULE"] = "benchmark.settings"
from django.conf import settings
from stream_framework.activity import Activity
from stream_framework.verbs.base import Add
from benchmark.feeds import UserFeed, TimelineFeed
from cassandra.cqlengine.management import sync_table, create_keyspace
from benchmark import tasks
import logging
from stream_framework.verbs import get_verb_storage
import boto3
import time
import click


logger = logging.getLogger()
handler = logging.StreamHandler()
handler.setFormatter(
    logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s"))
logger.addHandler(handler)
logger.setLevel('INFO')


def create_activity(user_id, object_id):
    verbs = get_verb_storage()
    verb = verbs.values()[user_id % len(verbs)]
    activity = Activity(
        user_id,
        verb,
        42,
    )
    return activity


class SocialModel(object):
    '''
    Basic assumptions about our social network
    '''
    active_users_percentage = 15
    
    def __init__(self, users=100):
        self.users = users
    
    @property
    def active_users(self):
        active_users = [u for u in range(1, self.users) if u % 100 < self.active_users_percentage]
        return active_users

    def get_user_activity(self, user_id):
        return 4
    
    def get_follower_ids(self, user_id):
        user_popularity = user_id % 10 + 1
        return range(5)



def validate_cloudformation_files():
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
        
        
def sync_cassandra():
    create_keyspace('stream_framework', 'SimpleStrategy', 3)
    for feed_class in [UserFeed, TimelineFeed]:
        timeline = feed_class.get_timeline_storage()
        sync_table(timeline.model)
        


@click.command()
@click.option('--start-users', default=10, help='Number of greetings.')
@click.option('--max-users', default=1000, help='Number of greetings.')
@click.option('--multiplier', default=2, help='Number of greetings.')
@click.option('--duration', default=3, help='Approximately the number of seconds to wait at every size of the userbase')
def run_benchmark(start_users, max_users, multiplier, duration):
    logger.info('Starting the benchmark! Exciting.... :)')
    logger.info('Running with settings %s', locals())
    sync_cassandra()
    logger.info('Synced the cassandra schema, all good')
    
    social_model = SocialModel(users=start_users)
    while True:
        logger.info('Simulating a social network with %s users', social_model.users)
        object_id = 1
        for x in range(duration):
            # create load based on the current model
            active_users = social_model.active_users
            for user_id in active_users:
                # follow other users
                for x in range(2):
                    tasks.follow_user(user_id, object_id % user_id)
                # create activities
                for x in range(social_model.get_user_activity(user_id)):
                    activity = create_activity(user_id, object_id)
                    object_id += 1
                    tasks.add_user_activity.delay(user_id, activity)
                # read a few pages of data
                tasks.read_feed_pages(user_id)
            time.sleep(1)
                
        # grow the network
        logger.info('Growing the social network.....')
        social_model.users = social_model.users * multiplier
        if social_model.users > max_users:
            logger.info('Reached the max users, we\'re done with our benchmark!')
        
        
        

if __name__ == '__main__':
    
    
    run_benchmark()
        
        
