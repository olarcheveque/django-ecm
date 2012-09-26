# -*- coding: utf-8 -*-

from ecm.core.views.base import ContentCreateView
from ecm.core.views.base import ContentFormsetView

from ecm.security.models import ACL
from ecm.security.forms import ACLFormSet


class WorkflowCreateView(ContentCreateView):

    def get_exclude(self):
        return list(self.exclude) + ['state_initial', ]


class SetupPermissionView(ContentFormsetView):
    actions = ()
    form_class = ACLFormSet

    def get_initial(self):
        ass_acls = ACL.granted_to.through.objects\
                .select_related('acl', 'ecmrole')\
                .filter(acl__state=self.object)

        acls = {}
        for ass_acl in ass_acls:
            if ass_acl.acl not in acls.keys():
                acls[ass_acl.acl] = []
            acls[ass_acl.acl].append(ass_acl.ecmrole)

        def get_acl_value(acl):
            if acl in acls.keys():
                return acls[acl]
            else:
                return []

        default_acls = ACL.objects\
                .select_related('state', 'permission', )\
                .filter(state=self.object)
        initial =  [{'permission': acl.permission, 'state': acl.state,
            'granted_to': get_acl_value(acl) } for acl in default_acls]
        return initial

    def get_template_names(self):
        return ("ecm/ecmstate/setup_permissions.html", )

    def save(self, form):
        permissions = self.get_initial()
        for i, f in enumerate(form):
            perm = permissions[i]['permission']
            state = permissions[i]['state']
            acl, created = ACL.objects.get_or_create(
                    state=state,
                    permission=perm)
            acl.granted_to = f.cleaned_data['granted_to']
            acl.save()
        
