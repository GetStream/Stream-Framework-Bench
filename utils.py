from math import atan, pi


def number_of_friends(active, network_size, scaling=1):
    """0:non_active, 1:active, 2:celebrity"""

    if active == 0:
        #No growth
        return 2
    if active == 1:
        avg_friends = 338 #steady state for active users
        #S-shaped growth on network size
        return avg_friends*(atan((network_size-250000000*scaling)/150000000*scaling) + pi/2)/pi
    if active == 2:
        #Linear growth on network size
        #Using katy perry's twitter info, 25% of all active users follow her
        proportion_active_users = .17
        return .25*network_size*proportion_active_users


def number_of_activities(active):

    if active == 0:
        return 0
    if active == 1:
        return 1
    if active == 2:
        return 2.5 #super rough estimate using Obama's twitter account


def number_of_pages(active, network_size, scaling=1):

    if active == 0:
        return 0
    if active == 1:
        avg_pages = 15 #steady state for active users
        #S-shaped growth on network size
        return avg_pages*(atan((network_size-250000000*scaling)/150000000*scaling) + pi/2)/pi
    if active == 2:
        return 5 #celebrities are too busy to spend all day on twitter?