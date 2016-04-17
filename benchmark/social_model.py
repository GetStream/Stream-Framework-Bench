from math import atan, pi


class SocialModel(object):

    '''
    Basic assumptions about our social network
    Nothing is random to ensure we create the same scenario every time we run the test
    '''
    VERSION = 0.1
    daily_active_users_percentage = 10

    def __init__(self, network_size=1000, day=1):
        self.network_size = network_size
        self.day = day

    @property
    def active_users(self):
        to_select = int(self.network_size * self.daily_active_users_percentage / 100.)
        active_users = range(1, to_select+1)
        return active_users

    def get_browse_depth(self, user_id):
        '''
        For a given active user_id
        How many pages does he read on a given day?
        '''
        bin_number = user_id % 100
        if 95 <= bin_number:
            return 50
        elif 85 <= bin_number < 95:
            return 20
        elif 75 <= bin_number < 85:
            return 10
        elif 50 <= bin_number < 75:
            return 5
        elif bin_number < 50:
            return 1

    def get_user_activity(self, user_id):
        '''
        For a given active user_id
        How many activities does this user produce during the day?
        '''
        bin_number = user_id % 100
        if 95 <= bin_number:
            return 25
        elif 85 <= bin_number < 95:
            return 10
        elif 75 <= bin_number < 85:
            return 5
        elif 50 <= bin_number < 75:
            return 1
        elif bin_number < 50:
            return 0

    def get_new_follows(self, user_id):
        '''
        For a given user
        How many new users do they follow during the day?
        '''
        bin_number = user_id % 100
        if 95 <= bin_number:
            new_follows = 25
        elif 85 <= bin_number < 95:
            new_follows = 10
        elif 75 <= bin_number < 85:
            new_follows = 5
        elif 50 <= bin_number < 75:
            new_follows = 1
        elif bin_number < 50:
            new_follows = 0
        # create a list of follow relationships based on new_follows 
        follower_ids = []
        for x in range(1, new_follows+1):
            follower_ids.append(self.network_size % (x*user_id))   
        
        return follower_ids

    def get_follower_ids(self, user_id, scaling=1):
        '''
        For a given user_id, how many followers does this user have?
        '''
        bin_number = user_id % 100
        if 98 <= bin_number:
            follower_percentage = 10
            follower_count = follower_percentage * self.network_size /100
            follower_count = max(follower_count, 1000)
        elif 85 <= bin_number < 98:
            follower_percentage = 5
            follower_count = follower_percentage * self.network_size /100
            follower_count = min(follower_count, 1000)
        elif 75 <= bin_number < 85:
            follower_count = 100
        elif 50 <= bin_number < 75:
            follower_count = 50
        elif bin_number < 50:
            follower_count = 5

        follower_ids = range(1, follower_count+1)
        return follower_ids
