# -*- coding: utf-8 -*-

from django import forms
from django.forms.formsets import formset_factory

from ecm.security.models import ECMRole, ACL
from widgets import CheckboxesAsCells

class ACLForm(forms.ModelForm):
    granted_to = forms.ModelMultipleChoiceField(
            queryset=ECMRole.objects.all(),
            widget=CheckboxesAsCells)

    class Meta:
        model = ACL
        exclude = ('state', 'permission', )


ACLFormSet = formset_factory(ACLForm, extra=0)
setattr(ACLFormSet, "headers", [r.title for r in ECMRole.objects.all()])
