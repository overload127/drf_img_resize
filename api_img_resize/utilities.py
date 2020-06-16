from datetime import datetime
from os.path import splitext


def get_timestamp_path(filename):
    """
    create name as Universally unique identifier from time
    """
    return '{0}{1}'.format(datetime.now().timestamp(), splitext(filename)[1])
