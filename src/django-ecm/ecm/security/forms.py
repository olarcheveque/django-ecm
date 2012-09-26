# -*- coding: utf-8 -*-

from django import forms
from django.forms.formsets import formset_factory

from ecm.security.models import ECMRole, ACL
from widgets import CheckboxesAsCells


def roles_sort_by_title():
    return ECMRole.objects.all().order_by('title')


class ACLForm(forms.ModelForm):
    granted_to = forms.ModelMultipleChoiceField(
            required=False,
            queryset=roles_sort_by_title(),
            widget=CheckboxesAsCells)

    class Meta:
        model = ACL
        exclude = ('state', )


ACLFormSet = formset_factory(ACLForm, extra=0)
ACLFormSet.headers = [r.title for r in roles_sort_by_title()]
