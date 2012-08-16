# -*- coding: utf-8 -*-

from django.db import models
from django.db.models import get_models
from django.db.models.signals import post_syncdb

from django.contrib.contenttypes.models import ContentType

from ecm.core import toc


class ECMWorkflow(models.Model):
    name = models.CharField(max_length=100)


class ECMState(models.Model):
    workflow = models.ForeignKey('ECMWorkflow')
    name = models.CharField(max_length=100)


class ECMTransition(models.Model):
    workflow = models.ForeignKey('ECMWorkflow')
    name = models.CharField(max_length=100)
    state_initial = models.ForeignKey('ECMState', related_name="+")
    state_final = models.ForeignKey('ECMState', related_name="+")


class ECMRole(models.Model):
    name = models.CharField(max_length=100)


class ECMPermission(models.Model):
    name = models.CharField(max_length=100)
    content_type = models.ForeignKey('contenttypes.ContentType')


def create_ecm_permissions(app, created_models, verbosity, **kwargs):
    app_models = get_models(app)

    for model in app_models:
        if model in toc.models:
            ct = ContentType.objects.get(model=model.__name__.lower())
            for perm in model.get_permissions():
                p, created = ECMPermission.objects.get_or_create(
                        name=perm, content_type=ct)
                if created:
                    print "permission '%s' created" % perm

post_syncdb.connect(create_ecm_permissions)
