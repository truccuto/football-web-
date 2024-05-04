from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from login.models import Team, Player_Stat, Player, Team_Stat, Coach
# Create your views here.
def index(request):
    teams_stat = Team_Stat.objects.all()
    ranked_teams = sorted(teams_stat, key=lambda team_stat: (team_stat.pts, team_stat.goals - team_stat.goalsconceded,team_stat.awaygoals),reverse=True)[:4]
    players_stat = Player_Stat.objects.all()
    ranked_players = sorted(players_stat, key=lambda player_stat: (player_stat.numberofgoals),reverse=True)[:3]
    team_list = Team.objects.all()
    username = request.user.username
    user = request.user
    context = {
        'ranked_teams': ranked_teams,
        'ranked_players': ranked_players,
        'username': username,
        'team_list': team_list,
        'user': user,
    }
    return render(request, 'pages/home.html',context)

def show_team(request):
    if request.method == 'POST':
        id = request.POST.get('teamid')
        team = Team.objects.get(pk=id)
        coach_exists = Coach.objects.filter(team=team).exists()
    username = request.user.username
    team_list = Team.objects.all()
    user = request.user
    context = {
        'username': username,
        'team_list': team_list,
        'team': team,
        'coach_exists': coach_exists,
        'user': user,
    }
    return render(request, 'pages/show_team.html',context)

def show_player(request):
    if request.method == 'POST':
        id = request.POST.get('playerid')
        player = Player.objects.get(pk=id)
    username = request.user.username
    user = request.user
    team_list = Team.objects.all()
    context = {
        'username': username,
        'team_list': team_list,
        'player': player,
        'user': user,
    }
    return render(request, 'pages/show_player.html',context)  

def logout_user(request):
    logout(request)
    return redirect('/login')