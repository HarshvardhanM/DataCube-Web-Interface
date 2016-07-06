from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm
from .models import *
# from codemirror2.widgets import CodeMirrorEditor
# from djangocodemirror.fields import CodeMirrorWidget

BANDS = [(1,"Blue"),(2,"Green"),(3,"Red"),(4,"Nir")]

class dataForm(forms.Form):
	year = forms.IntegerField(label="Year")
	layer = forms.ChoiceField(label="Layer",choices = BANDS)
	x1 = forms.CharField(max_length=8,label="x1")
	x2 = forms.CharField(max_length=8,label="x2")
	y1 = forms.CharField(max_length=8,label="y1")
	y2 = forms.CharField(max_length=8,label="y2")

# class CodeForm(forms.Form):
# 	code = forms.CharField(widget=CodeMirrorEditor(options={'mode': 'css'}))	

# class CodeForm2(forms.Form):
# 	code2 = forms.CharField(label="Your content", widget=CodeMirrorWidget(config_name='default'))