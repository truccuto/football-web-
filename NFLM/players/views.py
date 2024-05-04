from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.core.exceptions import ValidationError
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from .forms import PlayerForm, PlayerSearchForm
from login.models import Player,Team

# Create your views here.
def index(request):
    form = PlayerSearchForm(request.GET)
    player_list = Player.objects.select_related('team').all()
    team_list = Team.objects.all()
    username = request.user.username
    context = {
        'username': username,
        'team_list': team_list,
        'player_list': player_list,
        'form': form,
    }
    return render(request, 'pages/players.html',context)

def logout_user(request):
    logout(request)
    return redirect('/login')

def add_player(request):
    submitted = False
    if request.method == "POST":
        form = PlayerForm(request.POST, request.FILES)
        if form.is_valid():
            player = form.save()
            if 'image' in request.FILES:
                if player.image:
                    player.image.delete(save=False)
                player.image = request.FILES['image']
                player.image.name = f'player_{player.team.teamid}_{player.playerid}.png'
                player.save()

            return HttpResponseRedirect('/players/add_player?submitted=True')
    else:
        form = PlayerForm()
        if 'submitted' in request.GET:
            submitted = True
    username = request.user.username
    team_list = Team.objects.all()
    context = {
        'username': username,
        'form': form,
        'submitted': submitted,
        'team_list': team_list
    }
    return render(request, 'pages/add_player.html',context)

def show_player(request, player_id):
    player = Player.objects.get(pk=player_id)
    username = request.user.username
    team_list = Team.objects.all()
    context = {
        'username': username,
        'team_list': team_list,
        'player': player
    }
    return render(request, 'pages/show_player.html',context)  

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
            return redirect('/players')
    else:
        form = PlayerForm(instance=player)
    username = request.user.username
    team_list = Team.objects.all()
    context = {
        'username': username,
        'form': form,
        'team_list': team_list
    }
    return render(request, 'pages/add_player.html',context)

def delete_player(self, request, player_id):
    player = Player.objects.get(pk=player_id)
    if stat.numberofgoals > 0 or stat.numberofassits > 0:
        self.add_error('unable to delete player!')
    else:
        player.delete()
    return redirect('/players')

def search_player(request):
    form = PlayerSearchForm(request.GET)
    players = None
    if form.is_valid():
        player_name = form.cleaned_data['player_name']
        players = Player.objects.filter(name=player_name)
    username = request.user.username
    user = request.user
    team_list = Team.objects.all()
    context = {
        'username': username,
        'form': form,
        'team_list': team_list,
        'players': players,
        'user': user,
    }
    return render(request, 'pages/search_player.html', context)