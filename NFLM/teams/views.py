from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from .forms import TeamForm, PlayerForm, CoachForm, TeamSearchForm
from login.models import Team, Player, Coach, Regulation
from django.core.exceptions import ObjectDoesNotExist

# Create your views here.
def update_all_teams_status():
    regulation = Regulation.objects.get(pk=1)
    teams = Team.objects.all()
    for team in teams:
        team.update_status(maxforeignplayer=regulation.maxforeignplayer, maxplayer=regulation.maxplayer, minplayer=regulation.minplayer)
def index(request):
    form = TeamSearchForm(request.GET)
    update_all_teams_status()
    team_list = Team.objects.all()
    username = request.user.username
    user = request.user
    context = {
        'username': username,
        'team_list': team_list,
        'user': user,
        'form': form,
    }
    return render(request, 'pages/teams.html',context)

def logout_user(request):
    logout(request)
    return redirect('/login')

def add_team(request):
    submitted = False
    if request.method == "POST":
        form = TeamForm(request.POST, request.FILES)
        if form.is_valid():
            team = form.save()
            if 'team_image' in request.FILES:
                if team.team_image:
                    team.team_image.delete(save=False)
                team.team_image = request.FILES['team_image']
                team.team_image.name = f'team_{team.teamid}.png'
                team.save()
            return HttpResponseRedirect('/teams/add_team?submitted=True')
    else:
        form = TeamForm()
        if 'submitted' in request.GET:
            submitted = True
    username = request.user.username
    user = request.user
    team_list = Team.objects.all()
    context = {
        'username': username,
        'form': form,
        'submitted': submitted,
        'team_list': team_list,
        'user': user,
    }
    return render(request, 'pages/add_team.html',context)

def show_team(request, teamid):
    team = Team.objects.get(pk=teamid)
    coach_exists = Coach.objects.filter(team=team).exists()
    username = request.user.username
    user = request.user
    team_list = Team.objects.all()
    context = {
        'username': username,
        'team_list': team_list,
        'team': team,
        'coach_exists': coach_exists,
        'user': user,
    }
    return render(request, 'pages/show_team.html',context)  

def edit_team(request, team_id):
    team = Team.objects.get(pk=team_id)
    
    if request.method == "POST":
        form = TeamForm(request.POST, request.FILES, instance=team)
        if form.is_valid():
            team = form.save()
            if 'team_image' in request.FILES:
                if team.team_image:
                    team.team_image.delete(save=False)
                team.team_image = request.FILES['team_image']
                team.team_image.name = f'team_{team.teamid}.png'
                team.save()
            return redirect('/teams')
    else:
        form = TeamForm(instance=team)
    username = request.user.username
    user = request.user
    team_list = Team.objects.all()
    context = {
        'username': username,
        'form': form,
        'team_list': team_list,
        'user': user,
    }
    return render(request, 'pages/add_team.html',context)

def delete_team(request, team_id):
    team = Team.objects.get(pk=team_id)
    team.delete()
    return redirect('/teams')

def edit_coach(request, coach_id):
    coach = Coach.objects.get(pk=coach_id)
    
    if request.method == "POST":
        form = CoachForm(request.POST, request.FILES, instance=coach)
        if form.is_valid():
            coach = form.save()
            if 'coach_image' in request.FILES:
                if coach.coach_image:
                    coach.coach_image.delete(save=False)
                coach.coach_image = request.FILES['coach_image']
                coach.coach_image.name = f'coach_{coach.team.teamid}_{coach.coachid}.png'
                coach.save()
            return redirect('/teams')
    else:
        form = CoachForm(instance=coach)
    username = request.user.username
    team_list = Team.objects.all()
    user = request.user
    context = {
        'username': username,
        'form': form,
        'team_list': team_list,
        'user': user,
    }
    return render(request, 'pages/add_coach.html',context)

def delete_coach(request, coach_id):
    coach = Coach.objects.get(pk=coach_id)
    coach.delete()
    return redirect('/teams')

def edit_player(request, player_id):
    player = Player.objects.get(pk=player_id)
    
    if request.method == "POST":
        form = PlayerForm(request.POST, request.FILES, instance=player)
        if form.is_valid():
            player = form.save()
            if 'image' in request.FILES:
                if player.image:
                    player.image.delete(save=False)
                player.image = request.FILES['image']
                player.image.name = f'player_{player.team.teamid}_{player.playerid}.png'
                player.save()
            return redirect('/teams')
    else:
        form = PlayerForm(instance=player)
    username = request.user.username
    user = request.user
    team_list = Team.objects.all()
    context = {
        'username': username,
        'form': form,
        'team_list': team_list,
        'user': user,
    }
    return render(request, 'pages/add_player.html',context)

def delete_player(request, player_id):
    player = Player.objects.get(pk=player_id)
    player.delete()
    return redirect('/teams')

def search_team(request):
    form = TeamSearchForm(request.GET)
    teams = None
    if form.is_valid():
        team_name = form.cleaned_data['team_name']
        teams = Team.objects.filter(team_name=team_name)
    user = request.user
    username = request.user.username
    team_list = Team.objects.all()
    context = {
        'username': username,
        'form': form,
        'team_list': team_list,
        'teams': teams,
        'user': user,
    }
    return render(request, 'pages/search_team.html', context)