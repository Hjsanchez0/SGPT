from django import forms

#Create your forms here.
class LoginForm(forms.Form):
    username = forms.CharField(label='Username', max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)

class ReestablecerForm(forms.Form):
    email = forms.CharField(label='Email', max_length=200)

class ResetearForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)