"""
Usage:

SubmitButtonField(label="", initial=u"Your submit button text")
"""

from django import forms
from django.utils import html

class SubmitButtonWidget(forms.Form):
    COUNTRY=[('live','LIVE'),('staging','STAGING')]

    ENV = forms.ChoiceField(choices=COUNTRY, widget=forms.RadioSelect)


class SubmitButtonWidgetOne(forms.Form):
    TYPE=[('plp','PLP')]

    PAGE_TYPE = forms.ChoiceField(choices=TYPE, widget=forms.RadioSelect)