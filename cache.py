from functools import wraps
from werkzeug.contrib.cache import SimpleCache
from flask import current_app
cache = SimpleCache()


def cache_decorator(key_f, time=360):
    """
    key_f() - return key; type(key) == str
    """
    def wrapper(f):
        @wraps(f)
        def inner(*args, **kwargs):
            key = key_f()
            if cache.has(key):
                data = cache.get(key)
            else:
                data = f(*args, **kwargs)
                cache.set(key, data, timeout=time)
                current_app.logger.info('Cache set key %s' % key)
            return data
        return inner
    return wrapper

def clear_cache():
    cache.clear()
    current_app.logger.info('Cache cleared')