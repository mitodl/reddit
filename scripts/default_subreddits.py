# Usage:
#    To list default subreddits:
#       sudo reddit-run scripts/default_subreddits.py -c 'list_default_subreddits()'
#    To set default subreddits:
#       sudo reddit-run scripts/default_subreddits.py -c 'set_default_subreddits("one", "two", "three")'
#    To add a default subreddit:
#       sudo reddit-run scripts/default_subreddits.py -c 'add_default_subreddit("four")'
#    To remove a default subreddit:
#       sudo reddit-run scripts/default_subreddits.py -c 'remove_default_subreddit("five")'
#
from r2.models import LocalizedDefaultSubreddits, LocalizedFeaturedSubreddits
from r2.models.subreddit import Subreddit


def _get_default_subreddits():
    return set(Subreddit._byID(sr_id).name for sr_id in LocalizedDefaultSubreddits.get_global_defaults())


def list_default_subreddits():
    print( _get_default_subreddits())


def add_default_subreddit(sr_id_to_add):
    sr_ids = _get_default_subreddits()

    if sr_id_to_add not in sr_ids:
        print("adding default subreddit: {}".format(sr_id_to_add))
        sr_ids.add(sr_id_to_add)
        set_default_subreddits(*sr_ids)
    else:
        print("subreddit is already a default")


def remove_default_subreddit(sr_id_to_remove):
    sr_ids = _get_default_subreddits()
    if sr_id_to_remove in sr_ids:
        print("removing default subreddit: {}".format(sr_id_to_remove))
        sr_ids.remove(sr_id_to_remove)
        set_default_subreddits(*sr_ids)
    else:
        print("subreddit is not currently a default")


def set_default_subreddits(*sr_ids):
    print("setting default subreddits")
    srs = [Subreddit._by_name(sr_id) for sr_id in sr_ids]
    LocalizedDefaultSubreddits.set_global_srs(srs)
    LocalizedFeaturedSubreddits.set_global_srs(srs)
    print("default subreddits set to: {}".format(sr_ids))
