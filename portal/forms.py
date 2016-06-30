from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm
from .models import *

BANDS = [(1,"Blue"),(2,"Green"),(3,"Red"),(4,"Nir")]

class dataForm(forms.Form):
	year = forms.IntegerField(label="Year")
	layer = forms.ChoiceField(label="Layer",choices = BANDS)
	x1 = forms.CharField(max_length=8,label="x1")
	x2 = forms.CharField(max_length=8,label="x2")
	y1 = forms.CharField(max_length=8,label="y1")
	y2 = forms.CharField(max_length=8,label="y2")