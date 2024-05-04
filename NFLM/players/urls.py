from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views
urlpatterns = [
    path('', views.index),
    path('logout_user', views.logout_user, name='logout'),
    path('add_player', views.add_player, name='add-player'),
    path('show_player/<int:player_id>/', views.show_player, name='show-player'),
    path('player/edit/<int:player_id>/', views.edit_player, name='edit-player'),
    path('player/delete/<int:player_id>/', views.delete_player, name='delete-player'),
    path('search/', views.search_player, name='search_player'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)