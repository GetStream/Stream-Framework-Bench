from math import atan, pi


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
        active_users = [u for u in range(
            1, self.users) if u % 100 < self.daily_active_users_percentage]
        return active_users

    def get_browse_depth(self, user_id):
        '''
        For a given user_id and network_size, how many pages does this user browse?
        '''
        network_size = self.users
        if network_size < 1000:
            return user_id % 2
        else:
            bin_number = user_id % 1000
            if 995 <= bin_number:
                return 50
            if 985 <= bin_number < 995:
                return 20
            if 965 <= bin_number < 985:
                return 10
            if 935 <= bin_number < 965:
                return 5
            if 735 <= bin_number < 935:
                return 1
            else:
                return 0

    def get_user_activity(self, user_id):
        '''
        For a given user_id, how many activities does this user produce during the day?
        '''
        bin_number = user_id % 1000
        if 995 <= bin_number:
            return 25
        if 985 <= bin_number < 995:
            return 10
        if 965 <= bin_number < 985:
            return 5
        if 935 <= bin_number < 965:
            return 2
        if 735 <= bin_number < 935:
            return 1
        else:
            return 0

    def get_new_follows(self, user_id):
        '''
        For a given user, how many new users do they follow during the day?
        '''
        return (user_id + 123456789) % self.users

    def get_follower_ids(self, user_id, network_size, scaling=1):
        '''
        For a given user_id, how many followers does this user have?
        This also depends on the network size
        '''
        bin_number = (user_id / network_size) * 100

        if bin_number <= 90:
            # No growth
            num_followers = 0
        if 89 < bin_number <= 99:
            avg_friends = 338  # steady state for active users
            # S-shaped growth on network size
            num_followers = avg_friends * \
                (atan((network_size - 250000000 * scaling) /
                      150000000 * scaling) + pi / 2) / pi

        else:
            # Linear growth on network size
            proportion_active_users = .1
            num_followers = .25 * network_size * proportion_active_users - .25 * \
                network_size / 2 * proportion_active_users

        user_popularity = user_id % 10 + 1
        follower_ids = range(num_followers)
        follower_ids = [(user_id * pi) %
                        network_size for user_id in follower_ids]
        return follower_ids
