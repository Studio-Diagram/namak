from django import forms

class CreateNewsForm(forms.Form):
    title = forms.CharField(label='Title', max_length=300, required=False)
    text = forms.CharField(label='Text', max_length=4000)
    link = forms.CharField(label='Link', max_length=300, required=False)

