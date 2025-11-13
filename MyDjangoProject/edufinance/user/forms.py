from django import forms


class LoginForm(forms.ModelForm):
    username = forms.CharField(max_length=200)
    password = forms.PasswordInput()