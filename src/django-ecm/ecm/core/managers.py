# -*- coding: utf-8 -*-

from mptt.managers import TreeManager


class ECMCatalogManager(TreeManager):

    def get_query_set(self):
        return super(ECMCatalogManager, self).get_query_set()\
                .select_related('content_type')
