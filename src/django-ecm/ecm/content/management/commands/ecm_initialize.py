# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand
from ecm.content.models import ECMSite
from ecm.security.models import ECMWorkflowFolder

class Command(BaseCommand):

    def handle(self, *args, **options):

        obj, created = ECMSite.objects.get_or_create(slug="ecm")
        if created:
            obj.title = "ECM"
            obj.save()
            self.stdout.write("'%s' successfully created\n" % obj.slug)

        obj, created = \
            ECMWorkflowFolder.objects.get_or_create(slug="workflows")
        if created:
            obj.title = "Workflows"
            obj.save()
            self.stdout.write("'%s' successfully created\n" % obj.slug)
