from benchmark.celery import app
from benchmark.manager import benchmark_manager
from stream_framework.utils import get_metrics_instance
from benchmark import feeds


@app.task(bind=True, ignore_result=True)
def add_activities(self, social_model, user_activity_tuples):
    for user_id, activity in user_activity_tuples:
        # inserts into cassandra and creates the fanout tasks
        follower_ids = social_model.get_follower_ids(user_id)
        benchmark_manager.add_user_activity(user_id, activity, follower_ids)


@app.task(bind=True, ignore_result=True)
def read_feed_pages(self, social_model, user_ids):
    for user_id in user_ids:
        browse_depth = social_model.get_browse_depth(user_id)
        feed_instance = feeds.TimelineFeed(user_id)
        metrics = get_metrics_instance()
        # browse x pages deep
        for page in range(browse_depth):
            # track the time every read takes
            with metrics.feed_reads_timer(feed_instance.__class__):
                activities = feed_instance[:25]
                if activities and len(activities) == 25:
                    last_id = activities[-1]
                    feed_instance.filter(id__lte=last_id)
                else:
                    break


@app.task(bind=True, ignore_result=True)
def follow_users(self, social_model, follows):
    # user a follows user b. since we're already in a task, run with
    # async=False
    for user_id, target_user_id in follows:
        benchmark_manager.follow_user(user_id, target_user_id, async=False)
