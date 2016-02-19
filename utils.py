from math import atan, pi


def number_of_pages(user_id, network_size):

    if network_size < 1000:
        return user_id % 2
    else:
        bin_number = (user_id/network_size)*1000
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


def number_of_friends(user_id, network_size, scaling=1):

    bin_number = (user_id/network_size)*100

    if bin_number <= 90:
        #No growth
        return 2
    if 89 < bin_number <= 99:
        avg_friends = 338 #steady state for active users
        #S-shaped growth on network size
        return avg_friends*(atan((network_size-250000000*scaling)/150000000*scaling) + pi/2)/pi
    else:
        #Linear growth on network size
        proportion_active_users = .17
        return .25*network_size*proportion_active_users


def number_of_activities(user_id, network_size):

    bin_number = (user_id/network_size)*100

    if bin_number <= 89:
        return 0
    if 89 < bin_number <= 98:
        return 1
    else:
        return 2.5 #super rough estimate using Obama's twitter account



