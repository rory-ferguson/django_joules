"""
Usage:

SubmitButtonField(label="", initial=u"Your submit button text")
"""

from django import forms
from django.utils import html

class SubmitButtonWidget(forms.Form):
    COUNTRY=[('live','LIVE'),('staging','STAGING')]
    TYPE=[('plp','PLP')]

    ENV = forms.ChoiceField(choices=COUNTRY, widget=forms.RadioSelect)
    PAGE_TYPE = forms.ChoiceField(choices=TYPE, widget=forms.RadioSelect)