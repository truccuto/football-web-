from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from .forms import CoachForm, CoachSearchForm
from login.models import Coach, Team
# Create your views here.
def index(request):
    form = CoachSearchForm(request.GET)
    coach_list = Coach.objects.all()
    team_list = Team.objects.all()
    username = request.user.username
    user = request.user
    context = {
        'username': username,
        'team_list': team_list,
        'coach_list': coach_list,
        'user': user,
        'form':form,
    }
    return render(request, 'pages/managers.html',context)

def logout_user(request):
    logout(request)
    return redirect('/login')

def add_coach(request):
    submitted = False
    if request.method == "POST":
        form = CoachForm(request.POST, request.FILES)
        if form.is_valid():
            coach = form.save()
            if 'coach_image' in request.FILES:
                if coach.coach_image:
                    coach.coach_image.delete(save=False)
                coach.coach_image = request.FILES['coach_image']
                coach.coach_image.name = f'coach_{coach.team.teamid}_{coach.coachid}.png'
                coach.save()
            return HttpResponseRedirect('/managers/add_coach?submitted=True')
    else:
        form = CoachForm()
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
    return render(request, 'pages/add_coach.html',context)

def show_coach(request, coach_id):
    coach = Coach.objects.get(pk=coach_id)
    username = request.user.username
    user = request.user
    team_list = Team.objects.all()
    context = {
        'user': user,
        'username': username,
        'team_list': team_list,
        'coach': coach
    }
    return render(request, 'pages/show_manager.html',context)

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
            return redirect('/managers')
    else:
        form = CoachForm(instance=coach)
    user = request.user
    username = request.user.username
    team_list = Team.objects.all()
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
    return redirect('/managers')

def search_coach(request):
    form = CoachSearchForm(request.GET)
    coach_list = None
    if form.is_valid():
        coach_name = form.cleaned_data['coach_name']
        coach_list = Coach.objects.filter(coach_name=coach_name)
    username = request.user.username
    user = request.user
    team_list = Team.objects.all()
    context = {
        'username': username,
        'form': form,
        'team_list': team_list,
        'coach_list': coach_list,
        'user': user,
    }
    return render(request, 'pages/search_manager.html', context)