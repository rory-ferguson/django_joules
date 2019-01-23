from django import forms

class NameForm(forms.Form):
    sku = forms.CharField(label='Product SKU', max_length=100)