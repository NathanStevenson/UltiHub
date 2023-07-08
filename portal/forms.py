from django import forms
from .models import *    

class AddTeamForm(forms.ModelForm):
    # This is the way to style Model Forms because the field isnt declared directly on the form
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Team Logo Input Design
        self.fields["team_logo"].widget.attrs.update({
            # Can take advantage of bootstrap with this
            "class": "text-center ms-4 mt-3",
            })

        
    
    team_logo = forms.ImageField(required=False)
    name = forms.CharField(required=False)
    level = forms.CharField(required=False)
    type = forms.CharField(required=False)
    email = forms.CharField(required=False)
    password = forms.CharField(required=False, widget=forms.PasswordInput)
    confirm_password = forms.CharField(required=False, widget=forms.PasswordInput)

    class Meta:
        model = Team
        fields = ['team_logo', 'name', 'level', 'type', 'email', 'password', 'confirm_password']
