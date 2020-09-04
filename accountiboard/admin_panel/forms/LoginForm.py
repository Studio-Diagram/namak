from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(label='Username', max_length=300, required=True)
    password = forms.CharField(label='Password', max_length=300, required=True)
