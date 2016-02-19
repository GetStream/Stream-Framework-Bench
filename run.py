import os
import sys
sys.path.insert(0, os.path.dirname(__file__))
os.environ["DJANGO_SETTINGS_MODULE"] = "benchmark.settings"
from django.conf import settings
from stream_framework.activity import Activity
from benchmark import tasks
import logging
from stream_framework.verbs.base import *
from stream_framework.verbs import get_verb_storage
import time
import click
from logging.config import dictConfig

logger = logging.getLogger('bench')

LOGGING_DICT = { 
    'version': 1,
    'disable_existing_loggers': True,
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
            'propagate': False
        },
        'bench': { 
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False
        },
    } 
}
dictConfig(LOGGING_DICT)

@click.command()
@click.option('--start-users', default=10, help='Number of greetings.')
@click.option('--max-users', default=1000, help='Number of greetings.')
@click.option('--multiplier', default=2, help='Number of greetings.')
@click.option('--duration', default=3, help='Approximately the number of seconds to wait at every size of the userbase')
def run_benchmark(start_users, max_users, multiplier, duration):
    logger.info('Starting the benchmark! Exciting.... :)')
    logger.info('Running with settings %s', locals())
    logger.info('Synced the cassandra schema, all good')
    
    social_model = SocialModel(users=start_users)
    days = 0
    while True:
        logger.info('Simulating a social network with %s users', social_model.users)
        object_id = 1
        for x in range(duration):
            days += 1
            logger.debug('Day %s for our network', days)
            # create load based on the current model
            active_users = social_model.active_users
            for user_id in active_users:
                # follow other users, note that we don't actually store the follower
                #  lists for this benchmark
                for x in range(social_model.get_new_follows(user_id)):
                    tasks.follow_user(social_model, user_id, object_id % user_id)
                # create activities
                for x in range(social_model.get_user_activity(user_id)):
                    activity = create_activity(user_id, object_id)
                    object_id += 1
                    tasks.add_user_activity.delay(social_model, user_id, activity)
                # read a few pages of data
                tasks.read_feed_pages(social_model, user_id)
            time.sleep(1)
                
        # grow the network
        logger.info('Growing the social network.....')
        social_model.users = social_model.users * multiplier
        if social_model.users > max_users:
            logger.info('Reached the max users, we\'re done with our benchmark!')


def sync_cassandra():
    from cassandra.cqlengine.management import sync_table, create_keyspace
    from benchmark.feeds import UserFeed, TimelineFeed
    create_keyspace('stream_framework_bench', 'SimpleStrategy', 3)
    for feed_class in [UserFeed, TimelineFeed]:
        timeline = feed_class.get_timeline_storage()
        sync_table(timeline.model)
        
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
    Nothing is random to ensure we create the same scenario every time we run the test
    
    Makes assumptions about:
    - How many activities do the active users create?
    - How many users follow these users?
    Average follow count should increase with network size up to a steady state of followers (S-shaped curve)
    Using Facebook numbers: Steady state average follow count = 338
    - How many pages do they request when browsing their feed?
    '''
    VERSION = 0.1
    daily_active_users_percentage = 10
    
    def __init__(self, users=100):
        self.users = users
    
    @property
    def active_users(self):
        active_users = [u for u in range(1, self.users) if u % 100 < self.daily_active_users_percentage]
        return active_users

    def get_browse_depth(self, user_id):
        '''
        For a given user_id, how many pages does this user browse?
        '''
        return 4
    
    def get_user_activity(self, user_id):
        '''
        For a given user_id, how many activities does this user produce during the day?
        '''
        return 4
    
    def get_new_follows(self, user_id):
        '''
        For a given user, how many new users do they follow during the day?
        '''
        return 2
    
    def get_follower_ids(self, user_id):
        '''
        For a given user_id, how many followers does this user have?
        This also depends on the network size
        '''
        user_popularity = user_id % 10 + 1
        return range(user_popularity)
    
        
if __name__ == '__main__':
    sync_cassandra()
    run_benchmark()
        
        
