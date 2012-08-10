# -*- coding: utf-8 -*-

from django.core.cache import cache

def cached(func, timeout=60*60):
    def cached_func(self):
        key = '%s_%s_%s' % (
                self.__class__.__name__,
                func.__name__,
                self.pk
                )
        value = cache.get(key)
        if value is None:
                value = func(self)
                cache.set(key, value, timeout)
        return value
    return cached_func
