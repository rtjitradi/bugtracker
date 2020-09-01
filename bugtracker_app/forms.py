from django import forms
from bugtracker_app.models import TicketModel


class LoginForm(forms.Form):
    username = forms.CharField(max_length=50)
    password = forms.CharField(widget=forms.PasswordInput)


class NewTicketForm(forms.ModelForm):
    class Meta:
        model = TicketModel
        fields = ['title', 'description']
