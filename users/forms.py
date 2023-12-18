from django import forms

class MemberRegistrationForm(forms.Form):
    member_id = forms.CharField(label='ID', max_length=255)
    passwd = forms.CharField(label='PASSWORD', widget=forms.PasswordInput)
    name = forms.CharField(label='NAME', max_length=255)
    email = forms.EmailField(label='Email')