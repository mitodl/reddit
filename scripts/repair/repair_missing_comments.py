#
# Usage:
#    To repair comment ids "0" - "5":
#       sudo reddit-run scripts/repair/repair_missing_comments.py -c 'repair_comment_range("0", "5")'
#

from r2.lib import amqp
from r2.lib.db.thing import NotFound
from r2.models.link import Comment


def repair_comment_range(comment_start_id, comment_end_id):
    """
    Repairs the specified range of comment_start_id

    Args:
        comment_start_id (str): starting comment id
        comment_end_id (str): ending comment id
    """
    # base 36 decode the ids
    comment_start_id = int(comment_start_id, 36)
    comment_end_id = int(comment_end_id, 36)
    for comment_id in xrange(comment_start_id, comment_end_id + 1):
        try:
            comment = Comment._byID(comment_id)
        except NotFound:
            print("Not found: {}".format(comment_id))
            continue

        if not comment._deleted:
            print("Fixing comment: {}".format(comment._fullname))
            amqp.add_item('commentstree_q', comment._fullname)

    # fire the tasks
    amqp.worker.join()
