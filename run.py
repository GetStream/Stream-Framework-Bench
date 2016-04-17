import os
import sys
sys.path.insert(0, os.path.dirname(__file__))
os.environ["DJANGO_SETTINGS_MODULE"] = "benchmark.settings"

from benchmark.bench import get_benchmark
from stream_framework.utils.timing import timer
import collections
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
@click.option('--benchmark', default=None, help='Which predefined benchmark to run')
@click.option('--network-size', default=1000, help='Starting network size')
@click.option('--max-network-size', default=1000000, help='Max network size')
@click.option('--multiplier', default=2, help='How fast the network grows')
@click.option('--duration', default=3, help='How many virtual days to spend at each size of the network')
def run_benchmark(benchmark, network_size, max_network_size, multiplier, duration):
    logger.info('Starting the benchmark! Exciting.... :)')
    
    if benchmark is None:
        benchmark_class = get_benchmark('stream_bench_custom')
        benchmark = benchmark_class(network_size, max_network_size, multiplier, duration)
    else:
        benchmark_class = get_benchmark(benchmark)
        benchmark = benchmark_class()
    
    logger.info('Running benchmark %s', benchmark.name)
    logger.info('Network size starting at %s will grow to %s', benchmark.network_size, benchmark.network_size)
    logger.info('Multiplier is set to %s and duration %s', benchmark.multiplier, benchmark.duration)
    metrics_instance = get_metrics_instance()

    social_model = benchmark.get_social_model()
    days = 0
    while True:
        logger.info(
            'Simulating a social network with network size %s', social_model.network_size)
        object_id = 1
        for x in range(benchmark.duration):
            days += 1
            social_model.day = days
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
                
            logger.debug('%s seconds spent creating the model', t.next())
            # send the daily tasks to celery
            batch_tasks = []
            for task, task_args in daily_tasks.items():
                c = task.chunks(task_args, 100)
                batch_tasks.append(c)
            job = group(batch_tasks)
            job.apply_async()
            task_counts = [(task.name.split('.')[-1], len(args)) for task, args in daily_tasks.items()]
            logger.debug('%s seconds spent sending %s tasks', t.next(), task_counts)
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
        social_model.network_size = social_model.network_size * benchmark.multiplier
        metrics_instance.on_network_size_change(social_model.network_size)
        if social_model.network_size >= benchmark.max_network_size:
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
