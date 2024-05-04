from django import forms
from django.forms import ModelForm
from login.models import Team, Team_Stat, Coach, Nation, Sponsor, Player, Player_Stat, Regulation
from django.forms import widgets
import datetime
from django.core.exceptions import ValidationError
from datetime import date
# Create a Player form

class TeamSearchForm(forms.Form):
    team_name = forms.CharField(label='Team Name', max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Search', 'name': 'team_name'}))

class TeamForm(ModelForm):
    class Meta:
        model = Team
        exclude = ['country','status']
    
    sponsors = forms.ModelMultipleChoiceField(queryset=Sponsor.objects.all())
    team_image = forms.ImageField(required=True)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add Bootstrap classes to form fields
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

    # Add Bootstrap classes to form labels
    def label_tag(self, label=None, attrs=None, label_suffix=None):
        attrs = attrs or {}
        attrs['class'] = 'form-label'
        return super().label_tag(label, attrs, label_suffix)

class PlayerForm(ModelForm):
    class Meta:
        model = Player
        exclude = ['player_type']
    
    dob = forms.DateField(widget=widgets.DateInput(attrs={'type': 'date'}), initial=datetime.date.today())
    image = forms.ImageField(required=True)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add Bootstrap classes to form fields
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

    # Add Bootstrap classes to form labels
    def label_tag(self, label=None, attrs=None, label_suffix=None):
        attrs = attrs or {}
        attrs['class'] = 'form-label'
        return super().label_tag(label, attrs, label_suffix)
    def save(self, commit=True):

        player = super().save(commit=commit)
        if commit:
            if player.nationality == player.team.country:
                player.player_type = 'local'
            else:
                player.player_type = 'foreign'
            player.save()
        else:
            player_stat = None
        return player

    def clean(self):
        cleaned_data = super().clean()
        dob = cleaned_data.get('dob')
        regulation = Regulation.objects.get(pk=1)
        # Kiểm tra tuổi cầu thủ hợp lệ hay không
        if dob:
            today = date.today()
            age = today.year - dob.year

            if age < regulation.minage or age > regulation.maxage:
                self.add_error('dob', "Invalid date of birth. Player's age must be between 16 and 40 years.")
        return cleaned_data

class CoachForm(ModelForm):
    class Meta:
        model = Coach
        fields = "__all__"
    
    coach_image = forms.ImageField(required=True)
    dob = forms.DateField(widget=widgets.DateInput(attrs={'type': 'date'}), initial=datetime.date.today())
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add Bootstrap classes to form fields
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

    # Add Bootstrap classes to form labels
    def label_tag(self, label=None, attrs=None, label_suffix=None):
        attrs = attrs or {}
        attrs['class'] = 'form-label'
        return super().label_tag(label, attrs, label_suffix)
    def clean(self):
        cleaned_data = super().clean()
        dob = cleaned_data.get('dob')
        regulation = Regulation.objects.get(pk=1)
        # Kiểm tra tuổi cầu thủ hợp lệ hay không
        if dob:
            today = date.today()
            age = today.year - dob.year

            if age < regulation.minage:
                self.add_error('dob', "Invalid date of birth. Manager's age must greater than "+ str(regulation.minage)+".")
    