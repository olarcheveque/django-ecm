# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand
from ecm.content.models import ECMSite
from ecm.security.models import ECMWorkflow, ECMWorkflowFolder
from ecm.security.models import ECMState, ECMTransition
from ecm.security.models import ECMRole, ECMRoleFolder
from ecm.security.roles import OWNER, ANONYMOUS, AUTHENTICATED


def create_content(klass, **kwargs):
    obj, created = klass.objects.get_or_create(**kwargs)
    if created:
        print "'%s' successfully created" % obj.slug
    return obj

class Command(BaseCommand):

    def handle(self, *args, **options):

        create_content(ECMSite, slug="ecm", title="ECM")

        wf_folder = create_content(ECMWorkflowFolder,
                slug="workflows", title="Workflows")
        wf_default = create_content(ECMWorkflow,
                slug="default", title="Default", parent=wf_folder)
        wf_draft = create_content(ECMState,
                slug="draft", title="Draft", parent=wf_default)
        wf_published = create_content(ECMState,
                slug="published", title="Published", parent=wf_default)
        create_content(ECMTransition,
                slug="publish",
                title="Publish",
                parent=wf_default,
                state_initial=wf_draft,
                state_final=wf_published,
                )
        create_content(ECMTransition,
                slug="unpublish",
                title="Unpublish",
                parent=wf_default,
                state_initial=wf_published,
                state_final=wf_draft,
                )

        role_folder = create_content(ECMRoleFolder,
                slug="roles", title="Roles")
        create_content(ECMRole,
                slug=ANONYMOUS, title=ANONYMOUS.title(), parent=role_folder)
        create_content(ECMRole,
                slug=AUTHENTICATED, title=AUTHENTICATED.title(), parent=role_folder)
        create_content(ECMRole,
                slug="administrator", title="Administrator",
                parent=role_folder)
        create_content(ECMRole,
                slug=OWNER, title=OWNER.title(),
                parent=role_folder)
        create_content(ECMRole,
                slug="manager", title="Manager",
                parent=role_folder)
