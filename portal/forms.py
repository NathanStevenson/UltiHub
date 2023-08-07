from django import forms
from .models import *    

# form for adding a new team to our database. used inside team_login.html
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


# model form for adding an event. used inside of add_event.html
class addEventForm(forms.ModelForm):
    date = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    event_name = forms.CharField(required=False)
    notes = forms.CharField(required=False)
    class Meta:
        model = Event
        fields = ['date', 'event_name', 'notes']
