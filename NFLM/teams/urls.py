from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views
urlpatterns = [
    path('', views.index),
    path('logout_user', views.logout_user, name='logout'),
    path('add_team', views.add_team, name='add-team'),
    path('show_team/<int:teamid>/', views.show_team, name='show-team'),
    path('manager/edit/<int:coach_id>/', views.edit_coach, name='edit-coach'),
    path('manager/delete/<int:coach_id>/', views.delete_coach, name='delete-coach'),
    path('player/edit/<int:player_id>/', views.edit_player, name='edit-player'),
    path('player/delete/<int:player_id>/', views.delete_player, name='delete-player'),
    path('team/edit/<int:team_id>/', views.edit_team, name='edit-team'),
    path('team/delete/<int:team_id>/', views.delete_team, name='delete-team'),
    path('search/', views.search_team, name='search_team'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)