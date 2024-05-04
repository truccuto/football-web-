from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views
urlpatterns = [
    path('', views.index),
    path('logout_user', views.logout_user, name='logout'),
    path('schedule_form', views.schedule_form, name='add-match'),
    path('add_scores/<int:fixture_id>/', views.add_scores, name='add_scores'),
    path('record_result/<int:fixture_id>/', views.record_result, name='record_result'),
    path('show_result/<int:fixture_id>/', views.show_result, name='show_result'),
    path('fixture/edit/<int:fixture_id>/', views.edit_fixture, name='edit-fixture'),
    path('fixture/delete/<int:fixture_id>/', views.remove_fixture, name='remove-fixture'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)