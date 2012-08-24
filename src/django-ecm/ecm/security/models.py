# -*- coding: utf-8 -*-

from django.db import models
from django.db.models import get_models
from django.db.models.signals import post_syncdb
from django.utils.translation import ugettext_lazy as _

from django.contrib.contenttypes.models import ContentType

from ecm.core import toc
from ecm.core.models import ECMBaseContent, ECMBaseFolder


class ECMWorkflowFolder(ECMBaseFolder):
    """
    """
    create_view = "ecm.security.views.workflows.WorkflowFolderCreateView"
    allowed_content_types = ('ecmworkflow', )

    def get_children(self):
        return ECMWorkflow.objects.all()
toc.register(ECMWorkflowFolder)


class ECMWorkflow(ECMBaseFolder):
    """
    """
    class Meta:
        verbose_name = _("Workflow")

    allowed_content_types = ('ecmstate', 'ecmtransition', )
    state_initial = models.ForeignKey('ECMState', related_name="+", null=True)
    
    @property
    def states(self):
        return self.get_descendants().\
                filter(content_type__model='ecmstate')

    @property
    def transitions(self):
        return self.get_descendants().\
                filter(content_type__model='ecmtransition')

toc.register(ECMWorkflow)

class ECMState(ECMBaseContent):

    class Meta:
        verbose_name = _("State")
toc.register(ECMState)

class ECMTransition(ECMBaseContent):

    class Meta:
        verbose_name = _("Transition")

    state_initial = models.ForeignKey('ECMState', related_name="+")
    state_final = models.ForeignKey('ECMState', related_name="+")
toc.register(ECMTransition)


class ECMRole(ECMBaseContent):
    pass


class ECMPermission(models.Model):
    title = models.CharField(max_length=255)
    model_type = models.ForeignKey('contenttypes.ContentType')


def create_ecm_permissions(app, created_models, verbosity, **kwargs):
    app_models = get_models(app)

    for model in app_models:
        if model in toc.models:
            try:
                ct = ContentType.objects.get(model=model.__name__.lower())
                for perm in model.get_permissions():
                    p, created = ECMPermission.objects.get_or_create(
                            title=perm, model_type=ct)
                    if created:
                        print "permission '%s' created" % perm
            except:
                pass
post_syncdb.connect(create_ecm_permissions)
