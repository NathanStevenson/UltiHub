from django import forms
from .models import *    

class AddTeamForm(forms.ModelForm):
    
    team_logo = forms.ImageField(required=False)
    name = forms.CharField(required=False)
    level = forms.CharField(required=False)
    type = forms.CharField(required=False)
    email = forms.CharField(required=False)
    password = forms.CharField(required=False)
    confirm_password = forms.CharField(required=False)

    class Meta:
        model = Team
        fields = ['team_logo', 'name', 'level', 'type', 'email', 'password', 'confirm_password']