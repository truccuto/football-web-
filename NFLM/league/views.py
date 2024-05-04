from django.shortcuts import render, redirect
from django.http import HttpResponse, FileResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from login.models import Team, Regulation, Team_Stat, Player_Stat, Fixture, Result, GoalEvent
from .forms import RegulationForm
from django.template.loader import get_template
from django.template import Context
from io import BytesIO
from xhtml2pdf import pisa
# from reportlab.pdfgen import canvas
# Create your views here.
def index(request):
    team_list = Team.objects.all()
    username = request.user.username
    user = request.user
    context = {
        'username': username,
        'team_list': team_list,
        'user': user,
    }
    return render(request, 'pages/league.html',context)

def logout_user(request):
    logout(request)
    return redirect('/login')

def view_regulation(request):
    regulation = Regulation.objects.get(pk=1)
    username = request.user.username
    user = request.user
    team_list = Team.objects.all()
    context = {
        'username': username,
        'team_list': team_list,
        'user': user,
        'regulation': regulation
    }
    return render(request, 'pages/view_regulation.html',context)

def edit_regulation(request):
    regulation = Regulation.objects.get(pk=1)
    
    if request.method == "POST":
        form = RegulationForm(request.POST, instance=regulation)
        if form.is_valid():
            regulation = form.save()
            return redirect('/league')
    else:
        form = RegulationForm(instance=regulation)
    username = request.user.username
    user = request.user
    team_list = Team.objects.all()
    context = {
        'username': username,
        'form': form,
        'team_list': team_list,
        'user': user,
    }
    return render(request, 'pages/change_regulation.html',context)

def standing(request):
    teams_stat = Team_Stat.objects.all()

    ranked_teams = sorted(teams_stat, key=lambda team_stat: (team_stat.pts, team_stat.goals - team_stat.goalsconceded,team_stat.awaygoals),reverse=True)
    username = request.user.username
    user = request.user
    team_list = Team.objects.all()
    context = {
        'username': username,
        'ranked_teams': ranked_teams,
        'team_list': team_list,
        'user': user,
    }
    return render(request, 'pages/standing.html',context)

def stat_record(request):
    players_stat = Player_Stat.objects.all()

    ranked_players = sorted(players_stat, key=lambda player_stat: (player_stat.numberofgoals),reverse=True)
    username = request.user.username
    user = request.user
    team_list = Team.objects.all()
    context = {
        'username': username,
        'ranked_players': ranked_players,
        'team_list': team_list,
        'user': user,
    }
    return render(request, 'pages/stat_record.html',context)

def report(request):
    fixture_list = Fixture.objects.all()
    teams_stat = Team_Stat.objects.all()
    ranked_teams = sorted(teams_stat, key=lambda team_stat: (team_stat.pts, team_stat.goals - team_stat.goalsconceded,team_stat.awaygoals),reverse=True)
    players_stat = Player_Stat.objects.all()
    ranked_players = sorted(players_stat, key=lambda player_stat: (player_stat.numberofgoals),reverse=True)
    username = request.user.username
    user = request.user
    team_list = Team.objects.all()
    context = {
        'username': username,
        'ranked_players': ranked_players,
        'fixture_list': fixture_list,
        'team_list': team_list,
        'user': user,
        'ranked_teams': ranked_teams,
    }
    return render(request, 'pages/report.html',context)

def export_to_pdf(request):
    # Tạo một file PDF mới
    buffer = BytesIO()

    # Vẽ nội dung vào file PDF
    template = get_template('pages/report_pdf.html')
    fixture_list = Fixture.objects.all()
    teams_stat = Team_Stat.objects.all()
    ranked_teams = sorted(teams_stat, key=lambda team_stat: (team_stat.pts, team_stat.goals - team_stat.goalsconceded,team_stat.awaygoals),reverse=True)
    players_stat = Player_Stat.objects.all()
    ranked_players = sorted(players_stat, key=lambda player_stat: (player_stat.numberofgoals),reverse=True)
    context = {
        'ranked_players': ranked_players,
        'fixture_list': fixture_list,
        'ranked_teams': ranked_teams,
    }
    html = template.render(context)
    # Chuyển đổi HTML thành PDF và lưu vào buffer
    pisa.CreatePDF(BytesIO(html.encode('UTF-8')), buffer)

    # Di chuyển con trỏ về đầu buffer
    buffer.seek(0)

    # Trả về file PDF như là một HTTP response
    response = FileResponse(buffer, as_attachment=True, filename='report.pdf')
    return response






