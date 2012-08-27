# -*- coding: utf-8 -*-

from django.utils.decorators import classonlymethod


class ECMEntryMixin:

    class Meta:
        abstract = True

    detail_view = "ecm.core.views.base.ContentDetailView"
    create_view = "ecm.core.views.base.ContentCreateView"
    update_view = "ecm.core.views.base.ContentUpdateView"
    delete_view = "ecm.core.views.base.ContentDeleteView"

    @property
    def class_verbose_name(self):
        return self._meta.verbose_name


class ECMNavigationMixin:
    display_in_navigation = True


class ECMPermissionMixin:
    default_permissions = [
            'view',
            'add',
            'edit',
            'delete',
            ]

    permissions = []

    @classonlymethod
    def get_permissions(cls):
        default = ["%s %s" % (p, cls.__name__) for p in
                cls.default_permissions]
        return default + list(cls.permissions)


class ECMFolderMixin:
    allowed_content_types = ()


