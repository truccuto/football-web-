from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views
urlpatterns = [
    path('', views.index),
    path('logout_user', views.logout_user, name='logout'),
    path('regulation/edit/', views.edit_regulation, name='edit-regulation'),
    path('standing', views.standing, name='standing'),
    path('stat_record', views.stat_record, name='stat_record'),
    path('regulation/view/', views.view_regulation, name='view-regulation'),
    path('report', views.report, name='report'),
    path('export-pdf/', views.export_to_pdf, name='export-pdf'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)