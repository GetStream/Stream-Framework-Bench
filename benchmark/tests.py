import unittest2
from benchmark.social_model import SocialModel
from collections import defaultdict, Counter


class ModelTest(unittest2.TestCase):
    '''
    Verify our Social Model makes sense
    '''
    def test_browse_depth(self):
        model = SocialModel(1000)
        stats = Counter()
        for active_user in model.active_users:
            depth = model.get_browse_depth(active_user)
            stats[depth] += 1
        print stats.most_common()

    def test_user_activity(self):
        model = SocialModel(1000)
        stats = Counter()
        for active_user in model.active_users:
            activity_count = model.get_user_activity(active_user)
            stats[activity_count] += 1
        print stats.most_common()
        
    def test_get_new_follows(self):
        model = SocialModel(1000)
        stats = Counter()
        for active_user in model.active_users:
            follows = model.get_new_follows(active_user)
            stats[len(follows)] += 1
        #print stats.most_common()
        
    def test_get_follower_ids(self):
        model = SocialModel(1000)
        stats = Counter()
        for active_user in model.active_users:
            followers = model.get_follower_ids(active_user)
            stats[len(followers)] += 1
        print stats.most_common()
        