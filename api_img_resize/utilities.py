from datetime import datetime
from os.path import splitext


def get_timestamp_path(instance, filename):
    return 'images/{0}{1}'.format(datetime.now().timestamp(), splitext(filename)[1])
