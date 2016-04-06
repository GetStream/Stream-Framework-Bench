import os
import sys
from stream_framework.utils.timing import timer
import collections
sys.path.insert(0, os.path.dirname(__file__))
os.environ["DJANGO_SETTINGS_MODULE"] = "benchmark.settings"

from benchmark.social_model import SocialModel
from stream_framework.utils import get_metrics_instance
from benchmark.utils import create_activity
from django.conf import settings
from benchmark import tasks
import logging
import time
from celery import group
import click


logger = logging.getLogger('bench')



@click.command()
@click.option('--start-users', default=10, help='Number of greetings.')
@click.option('--max-users', default=1000, help='Number of greetings.')
@click.option('--multiplier', default=2, help='Number of greetings.')
@click.option('--duration', default=3, help='Approximately the number of seconds to wait at every size of the userbase')
def run_benchmark(start_users, max_users, multiplier, duration):
    logger.info('Starting the benchmark! Exciting.... :)')
    logger.info('Running with settings %s', locals())
    logger.info('Synced the cassandra schema, all good')
    metrics_instance = get_metrics_instance()

    social_model = SocialModel(users=start_users)
    days = 0
    while True:
        logger.info(
            'Simulating a social network with %s users', social_model.users)
        object_id = 1
        for x in range(duration):
            days += 1
            daily_tasks = collections.defaultdict(list)
            t = timer()
            metrics_instance.on_day_change(days)
            logger.debug('Day %s for our network', days)
            # create load based on the current model
            active_users = social_model.active_users
            for user_id in active_users:
                # follow other users, note that we don't actually store the follower
                #  lists for this benchmark
                for target_user_id in social_model.get_new_follows(user_id):
                    daily_tasks[tasks.follow_user].append([social_model, user_id, target_user_id])
                    
                # create activities
                for x in range(social_model.get_user_activity(user_id)):
                    activity = create_activity(user_id, object_id)
                    object_id += 1
                    daily_tasks[tasks.add_user_activity].append([social_model, user_id, activity])
                # read a few pages of data
                daily_tasks[tasks.read_feed_pages].append([social_model, user_id])
                
            print t.next()
            # send the daily tasks to celery
            batch_tasks = []
            for task, task_args in daily_tasks.items():
                c = task.chunks(task_args, 100)
                batch_tasks.append(c)
            job = group(batch_tasks)
            job.apply_async()
            print t.next(), 'to process %s tasks' % len(daily_tasks)
            # wait
            #while True:
            #    if result.ready():
            #        break
            #    time.sleep(1)
            #    logger.debug('Waiting for day %s to finish' % days)
            
            logger.debug('Day %s finished', days)
            time.sleep(1)

        # grow the network
        logger.info('Growing the social network.....')
        social_model.users = social_model.users * multiplier
        metrics_instance.on_network_size_change(social_model.users)
        if social_model.users > max_users:
            logger.info(
                'Reached the max users, we\'re done with our benchmark!')


def sync_cassandra():
    from cassandra.cqlengine.management import sync_table, create_keyspace
    from benchmark.feeds import UserFeed, TimelineFeed
    create_keyspace('stream_framework_bench', 'SimpleStrategy', 3)
    for feed_class in [UserFeed, TimelineFeed]:
        timeline = feed_class.get_timeline_storage()
        sync_table(timeline.model)


if __name__ == '__main__':
    sync_cassandra()
    run_benchmark()
