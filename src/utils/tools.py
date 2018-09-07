def caching(func):
    memCache = {}
    def wrapper(*args, **kwargs):
        if args in memCache:
            return memCache[args]
        res = func(*args, **kwargs)
        memCache[args] = res
        return res
    return wrapper
