from stream_framework.feed_managers.base import Manager, FanoutPriority
from benchmark import feeds


class BenchManager(Manager):
    feed_classes = {
        'timeline': feeds.TimelineFeed,
    }
    user_feed_class = feeds.UserFeed
    follow_activity_limit = 360
    fanout_chunk_size = 100

    def get_user_follower_ids(self, user_id):
        return {FanoutPriority.HIGH: self.follower_ids}

    def add_user_activity(self, user_id, activity, follower_ids):
        # convenient way to overwrite the follower ids
        self.follower_ids = follower_ids
        Manager.add_user_activity(self, user_id, activity)

benchmark_manager = BenchManager()
