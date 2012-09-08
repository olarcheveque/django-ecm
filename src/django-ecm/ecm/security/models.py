# -*- coding: utf-8 -*-

from django.db import models
from django.db.models import get_models
from django.db.models.signals import post_syncdb
from django.utils.translation import ugettext_lazy as _

from django.contrib.contenttypes.models import ContentType

from ecm.core import toc
from ecm.core.models import ECMBaseContent, ECMBaseFolder
from ecm.core.decorators import cached

class ECMWorkflowFolder(ECMBaseFolder):
    """
    """
    allowed_content_types = ('ecmworkflow', )

    @property
    def workflows(self):
        return self.get_descendants().\
                filter(content_type__model='ecmworkflow')
toc.register(ECMWorkflowFolder)


class ECMWorkflow(ECMBaseFolder):
    """
    """
    create_view = 'ecm.security.views.workflows.WorkflowCreateView'

    class Meta:
        verbose_name = _("Workflow")

    allowed_content_types = ('ecmstate', 'ecmtransition', )
    state_initial = models.ForeignKey('ECMState', related_name="+", null=True)
    
    @property
    def states(self):
        ids = [c.id for c in self.get_descendants().\
                filter(content_type__model='ecmstate')]
        return ECMState.objects.filter(id__in=ids)

    @property
    def transitions(self):
        ids = [c.id for c in self.get_descendants().\
                filter(content_type__model='ecmtransition')]
        return ECMTransition.objects.filter(id__in=ids)

toc.register(ECMWorkflow)

class ECMState(ECMBaseContent):

    class Meta:
        verbose_name = _("State")

    setup_permissions_view = 'ecm.security.views.workflows.SetupPermissionView'
    display_in_navigation = False

    @cached
    @models.permalink
    def get_absolute_setup_permissions_url(self):
        slugs = self.get_traversal_slugs()
        url = "/".join(slugs)
        return ('state_setup_permissions', [url, ])
toc.register(ECMState)


class ACL(models.Model):
    state = models.ForeignKey("ECMState", related_name="+")
    permission = models.ForeignKey("ECMPermission", related_name="+")
    granted_to = models.ManyToManyField("ECMRole")

    class Meta:
        verbose_name = _("ACL")


class ECMTransition(ECMBaseContent):

    class Meta:
        verbose_name = _("Transition")

    display_in_navigation = False

    state_initial = models.ForeignKey('ECMState', related_name="+")
    state_final = models.ForeignKey('ECMState', related_name="+")
toc.register(ECMTransition)


class ECMRoleFolder(ECMBaseFolder):
    """
    """
    allowed_content_types = ('ecmrole', )
toc.register(ECMRoleFolder)


class ECMRole(ECMBaseContent):

    class Meta:
        verbose_name = _("Role")
        ordering = ("title", )

class ECMPermission(ECMBaseContent):
    model_type = models.ForeignKey('contenttypes.ContentType')
    display_in_navigation = False


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
