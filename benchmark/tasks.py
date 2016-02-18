from benchmark.celery import app
from benchmark import manager
from benchmark import feeds

@app.task(bind=True)
def add_user_activity(self, user_id, activity):
    # inserts into cassandra and creates the fanout tasks
    manager.add_user_activity(user_id, activity)


@app.task(bind=True)
def read_feed(self, user_id):
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