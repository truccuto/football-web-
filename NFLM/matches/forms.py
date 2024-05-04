from django import forms
from django.forms import ModelForm
from login.models import Fixture, Team, Round, Stadium, Result, GoalEvent, Player, Regulation, Status
from django.forms import widgets
from django.utils import timezone
import datetime
from django.core.exceptions import ValidationError
from django.forms import formset_factory, BaseFormSet
# Create a Player form

class GoalEventForm(forms.ModelForm):
    class Meta:
        model = GoalEvent
        fields = ['player', 'assist_player' ,'goal_type', 'goal_time']
    def clean(self):
        cleaned_data = super().clean()
        goal_time = cleaned_data.get('goal_time')
        regulation = Regulation.objects.get(pk=1)
        if goal_time and goal_time > regulation.scoretime:
            self.add_error('goal_time', "Invalid goal time. Goal time must be scored < " + str(regulation.scoretime) +".")
        
        player = cleaned_data.get('player')
        assist_player = cleaned_data.get('assist_player')
        goal_type = cleaned_data.get('goal_type')
        
        if player and assist_player and player == assist_player and goal_type != 'Own Goal':
            player.player_stat.numberofassists -= 1
        return cleaned_data

class RecordResultForm(forms.Form):
    class Meta:
        model = Result
        fields = "__all__"
    team1pts = forms.IntegerField(label='Team 1 Points')
    team2pts = forms.IntegerField(label='Team 2 Points')


class RoundNameForm(ModelForm):
    class Meta:
        model = Round
        fields = "__all__"

class MatchForm(ModelForm):
    class Meta:
        model = Fixture
        fields = "__all__"
    round_name = forms.ModelChoiceField(queryset=Round.objects.all(), widget=forms.HiddenInput(), required=False)
    
    stadium = forms.ModelChoiceField(queryset=Stadium.objects.all(), widget=forms.HiddenInput(), required=False)
    status = forms.ModelChoiceField(queryset=Status.objects.all(), initial=Status.objects.get(statusname='Upcoming'), widget=forms.HiddenInput())
    team1 = forms.ModelChoiceField(queryset=None)
    team2 = forms.ModelChoiceField(queryset=None)
    time = forms.DateTimeField(widget=widgets.DateTimeInput(attrs={'type': 'datetime-local'}),initial=datetime.datetime.now().strftime("%Y-%m-%dT%H:%M"))
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['team1'].queryset = Team.objects.filter(status='MeetRequirements')
        self.fields['team2'].queryset = Team.objects.filter(status='MeetRequirements')
    
    def clean(self):
        cleaned_data = super().clean()
        team1 = cleaned_data.get('team1')
        team2 = cleaned_data.get('team2')
        time = cleaned_data.get('time')

        if team1 and team2 and team1 == team2:
            raise ValidationError("Team 1 and Team 2 cannot be the same.")
        
        if time:
            if time < timezone.now():
                cleaned_data['status'] = Status.objects.get(statusname='Done')
            else:
                cleaned_data['status'] = Status.objects.get(statusname='Upcoming')
        return cleaned_data
total_teams = Team.objects.count()
FixtureFormSet = formset_factory(MatchForm, extra=total_teams//total_teams)
    