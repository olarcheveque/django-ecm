# -*- coding: utf-8 -*-

from django.forms import ModelForm

class ContentForm(ModelForm):
    
    class Meta:
        exclude = ('parent', )

