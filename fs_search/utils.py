from functools import wraps, lru_cache

def memoize(func):
    cache = {}

    @wraps(func)
    def wrapper(*args, **kwargs):
        key = str(args) + str(kwargs)
        
        if key not in cache:
            cache[key] = func(*args, **kwargs)
        
        return cache[key]

    return wrapper

@memoize
def fibonacci(n) -> int:
    if n < 2:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)
