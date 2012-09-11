# -*- coding: utf-8 -*-

from ecm.security.models import ECMRole
from roles import AUTHENTICATED, ANONYMOUS, OWNER

def who_what(iterable, user=None, obj=None):
    for i in iterable:
        i.user = user
        i.obj = obj
    return iterable

def auth(user, obj):
    if user.is_anonymous():
        return who_what([ECMRole.objects.get(slug=ANONYMOUS), ], user, obj)
    else:
        return who_what([ECMRole.objects.get(slug=AUTHENTICATED), ], user, obj)


def owner(user, obj):
    if user.is_anonymous():
        return []
    else:
        for field in ('owner', 'user', ):
            owner = getattr(obj, 'owner', None)
            if owner is not None and user == owner:
                return who_what([ECMRole.objects.get(slug=OWNER), ], user, obj)
        return []
