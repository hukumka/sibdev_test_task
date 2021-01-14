from django.core.cache import caches


def tagged_cache(tag, timeout):
    """
    Add tagged cache to view
    """
    def decorator(func):
        def result(request):
            cache = caches['default']
            value = cache.get(tag)
            if value is None:
                res = func(request).render()
                cache.set(tag, res, timeout)
                value = res
            return value
        return result
    return decorator


def invalidate_cache(tag):
    cache = caches['default']
    cache.delete(tag)
