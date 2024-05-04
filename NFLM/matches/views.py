from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from login.models import Team, Fixture, Round, Result, GoalEvent, Team_Stat, Player, Regulation, Status
from .forms import MatchForm, FixtureFormSet, RoundNameForm, RecordResultForm, GoalEventForm
from django.utils import timezone
from django.forms import formset_factory
from django.core.exceptions import ObjectDoesNotExist
# Create your views here.
def index(request):
    team_list = Team.objects.all()
    fixture_list = Fixture.objects.all()
    for fixture in fixture_list:
        if fixture.time < timezone.now():
            fixture.status = Status.objects.get(statusname='Done')
        else:
            fixture.status = Status.objects.get(statusname='Upcoming')
        fixture.save()
    username = request.user.username
    user = request.user
    context = {
        'username': username,
        'team_list': team_list,
        'fixture_list': fixture_list,
        'user': user,
    }
    return render(request, 'pages/matches.html',context)

def logout_user(request):
    logout(request)
    return redirect('/login')

def schedule_form(request):
    submitted = False
    if request.method == 'POST':
        formset = FixtureFormSet(request.POST)
        round_name_form = RoundNameForm(request.POST)
        if formset.is_valid() and round_name_form.is_valid():
            round_name = round_name_form.cleaned_data['round_name']
            round_instance = Round(round_name=round_name)
            round_instance.save()
            for form in formset:
                team1 = form.cleaned_data['team1']
                team2 = form.cleaned_data['team2']
                if team1.status == 'NotMeetRequirement' or team2.status == 'NotMeetRequirement':
                    continue
                team = Team.objects.get(team_name=form.cleaned_data['team1'])
                fixture = form.save(commit=False)
                fixture.round_name = round_instance
                fixture.stadium = team.stadium
                fixture.save()
            return HttpResponseRedirect('/matches')
    else:
        formset = FixtureFormSet()
        round_name_form = RoundNameForm()
        if 'submitted' in request.GET:
            submitted = True
    username = request.user.username
    user = request.user
    team_list = Team.objects.all()
    context = {
        'username': username,
        'formset': formset,
        'team_list': team_list,
        'round_name_form': round_name_form,
        'user': user,
    }
    return render(request, 'pages/add_matches.html', context)

def add_scores(request, fixture_id):
    fixture = get_object_or_404(Fixture, pk=fixture_id)
    regulation = Regulation.objects.get(pk=1)
    if request.method == 'POST':
        form = RecordResultForm(request.POST)
        if form.is_valid():
            team1pts = form.cleaned_data['team1pts']
            team2pts = form.cleaned_data['team2pts']
            result = Result.objects.create(
                team1pts=team1pts,
                team2pts=team2pts,
                fixture=fixture
            )
            result.update_team_scores(winpts=regulation.winpts,losepts=regulation.losepts,drawpts=regulation.drawpts)
            return redirect('/matches')
    else:
        form = RecordResultForm()
    username = request.user.username
    user = request.user
    team_list = Team.objects.all()
    context = {
        'form': form,
        'fixture': fixture,
        'username': username,
        'team_list': team_list,
        'user': user,
    }

    return render(request, 'pages/add_scores.html', context)

def edit_fixture(request, fixture_id):
    fixture = get_object_or_404(Fixture, pk=fixture_id)
    if request.method == 'POST':
        form = MatchForm(request.POST, instance=fixture)
        if form.is_valid():
            form.save()
            return redirect('/matches')
    else:
        form = MatchForm(instance=fixture)
    username = request.user.username
    user = request.user
    team_list = Team.objects.all()
    context = {
        'form': form,
        'fixture': fixture,
        'username': username,
        'team_list': team_list,
        'user': user,
    }
    return render(request, 'pages/edit_match.html', context)

def remove_fixture(request, fixture_id):
    fixture = get_object_or_404(Fixture, pk=fixture_id)
    fixture.delete()
    return redirect('/matches')

def record_result(request, fixture_id):
    fixture = get_object_or_404(Fixture, pk=fixture_id)
    result, created = Result.objects.get_or_create(fixture_id=fixture_id)
    if request.method == 'POST':
        GoalEventFormSet = formset_factory(GoalEventForm, extra=0)
        formset = GoalEventFormSet(request.POST)
        if formset.is_valid():
            for form in formset:
                if form.has_changed():
                    goal_event = form.save(commit=False)
                    goal_event.result = result
                    goal_event.team = result.fixture.team1 if goal_event.player.team == result.fixture.team1 else result.fixture.team2
                    goal_event.save()
                    if goal_event.goal_type != 'Own Goal':
                        goal_event.update_player_stats()
            return redirect('/matches') # Đổi thành URL mong muốn
    else:
        GoalEventFormSet = formset_factory(GoalEventForm, extra=result.team1pts+result.team2pts)
        formset = GoalEventFormSet()
        # Lọc cầu thủ thuộc team1 hoặc team2
        team1_players = Player.objects.filter(team=fixture.team1)
        team2_players = Player.objects.filter(team=fixture.team2)
        valid_players = team1_players | team2_players
        for form in formset:
            form.fields['player'].queryset = valid_players
            form.fields['assist_player'].queryset = valid_players
    
    username = request.user.username
    user = request.user
    team_list = Team.objects.all()
    context = {
        'formset': formset,
        'fixture': fixture,
        'username': username,
        'team_list': team_list,
        'user': user,
    }

    return render(request, 'pages/record_result.html', context)

def show_result(request, fixture_id):
    fixture = get_object_or_404(Fixture, pk=fixture_id)
    try:
        result = Result.objects.get(fixture_id=fixture_id)
        goal_events = GoalEvent.objects.filter(result=result)
    except ObjectDoesNotExist:
        result = None
        goal_events = None
    username = request.user.username
    user = request.user
    team_list = Team.objects.all()
    context = {
        'result': result,
        'fixture': fixture,
        'username': username,
        'team_list': team_list,
        'goal_events': goal_events,
        'user': user,
    }

    return render(request, 'pages/show_result.html', context)
