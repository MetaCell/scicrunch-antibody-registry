import logging
from timeit import default_timer as timer


def timed_class_method(message):
    def wrapper(method):
        def wrapped(*args, **kwargs):
            start = timer()
            res = method(*args, **kwargs)
            end = timer()
            logging.info(f"{message} ({end - start} seconds)")
            return res
        return wrapped
    return wrapper
