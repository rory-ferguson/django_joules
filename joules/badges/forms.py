"""
Usage:

SubmitButtonField(label="", initial=u"Your submit button text")
"""

from django import forms
from django.utils import html

class SubmitButtonWidget(forms.Form):
    CHOICES=[('live','LIVE'),('staging','STAGING')]

    ENV = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect)
