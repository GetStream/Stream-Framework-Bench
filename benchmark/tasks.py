from benchmark.celery import app
from benchmark.manager import benchmark_manager
from benchmark import feeds

@app.task(bind=True, ignore_result=True)
def add_user_activity(self, user_id, activity, social_model):
    # inserts into cassandra and creates the fanout tasks
    follower_ids = social_model.get_follower_ids(user_id)
    benchmark_manager.add_user_activity(user_id, activity, follower_ids)


@app.task(bind=True, ignore_result=True)
def read_feed_pages(self, user_id):
    browse_depth = user_id % 5 + 1
    feed_instance = feeds.TimelineFeed(user_id)

    # browse x pages deep    
    for page in range(browse_depth):
        activities = feed_instance[:25]
        if activities and len(activities) == 25:
            last_id = activities[-1]
            feed_instance.filter(id__lte=last_id)
        else:
            break
        
@app.task(bind=True, ignore_result=True)
def follow_user(self, user_id, target_user_id):
    # user a follows user b. since we're already in a task, run with async=False
    benchmark_manager.follow_user(user_id, target_user_id, async=False)