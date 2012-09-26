# -*- coding: utf-8 -*-

from ecm.security.models import ECMRole, Owner, SuperuserRole
from roles import AUTHENTICATED, ANONYMOUS


def superuser(user):
    if user.is_superuser:
        return [SuperuserRole(), ]
    else:
        return []

def auth(user):
    if user.is_anonymous():
        slug = ANONYMOUS
    else:
        slug = AUTHENTICATED
    return ECMRole.objects.filter(slug=slug)


def owner(user):
    if user.is_authenticated():
        return Owner.objects.filter(user=user)
    else:
        return []
