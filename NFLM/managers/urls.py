from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views
urlpatterns = [
    path('', views.index),
    path('logout_user', views.logout_user, name='logout'),
    path('add_coach', views.add_coach, name='add-coach'),
    path('show_coach/<int:coach_id>/', views.show_coach, name='show-coach'),
    path('manager/edit/<int:coach_id>/', views.edit_coach, name='edit-coach'),
    path('manager/delete/<int:coach_id>/', views.delete_coach, name='delete-coach'),
    path('search/', views.search_coach, name='search_coach'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)