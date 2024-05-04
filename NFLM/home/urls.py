from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views
urlpatterns = [
    path('', views.index),
    path('logout_user', views.logout_user, name='logout'),
    path('show_player', views.show_player, name='show-player'),
    path('show_team', views.show_team, name='show-team'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)