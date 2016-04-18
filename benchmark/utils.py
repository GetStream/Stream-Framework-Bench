from stream_framework.verbs import get_verb_storage
from stream_framework.activity import Activity
from stream_framework.verbs.base import *
import itertools


def create_activity(user_id, object_id):
    '''
    Create a fake activity
    '''
    verbs = get_verb_storage()
    verb = verbs.values()[user_id % len(verbs)]
    activity = Activity(
        user_id,
        verb,
        42,
    )
    return activity


def chunks(iterable, n=10000):
    it = iter(iterable)
    while True:
        chunk = tuple(itertools.islice(it, n))
        if not chunk:
            return
        yield chunk
