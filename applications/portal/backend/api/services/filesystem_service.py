import os
import time
from datetime import datetime

from portal.settings import MAX_TRIES


def replace_file(previous_path, new_path, max_tries=MAX_TRIES):
    # replace original file with temp file
    os.remove(previous_path)
    tries = 0
    while not os.path.exists(new_path) and tries < max_tries:
        time.sleep(1)
        tries += 1
    os.rename(new_path, previous_path)


def check_if_file_does_not_exist_and_recent(fname):
    """not (exist and recent) => not exist or not recent""" 
    return not os.path.exists(fname) or (datetime.now() - datetime.fromtimestamp(os.path.getmtime(fname))).days > 1
