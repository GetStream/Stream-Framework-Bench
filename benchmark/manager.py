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
        active_follower_ids = range(100)
        return {FanoutPriority.HIGH: active_follower_ids}
    
manager = BenchManager()