# define the benchmark decorator
import logging
from datetime import timedelta
from functools import wraps
from time import perf_counter


def timed(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        t0 = perf_counter()
        res = func(*args, **kwargs)
        t1 = perf_counter()
        td = t1 - t0

        log = logging.getLogger(__name__)
        log.info(f"{func.__name__} | {timedelta(seconds=td)} | {res:>20} | ")

        return res

    return wrapper
