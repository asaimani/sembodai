from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('candidates/', views.candidate_list, name='candidate_list'),
    path('candidates/add/', views.candidate_add, name='candidate_add'),
    path('candidates/<str:gender>/<int:pk>/', views.candidate_detail, name='candidate_detail'),
    path('candidates/<str:gender>/<int:pk>/edit/', views.candidate_edit, name='candidate_edit'),
    path('candidates/<str:gender>/<int:pk>/print/', views.candidate_print, name='candidate_print'),
    path('api/nachathirams/', views.get_nachathirams, name='get_nachathirams'),
    path('api/sub_castes/', views.get_sub_castes, name='get_sub_castes'),
    path('api/districts/', views.get_districts, name='get_districts'),
    path('photos/<int:photo_id>/delete/', views.delete_photo, name='delete_photo'),
    path('candidates/<str:gender>/<int:pk>/delete/', views.candidate_delete, name='candidate_delete'),
    path('candidates/<str:gender>/<int:pk>/expectation/', views.save_expectation, name='save_expectation'),
    path('weekly-send/', views.weekly_send, name='weekly_send'),
    path('weekly-send/mark-sent/<str:log_ids>/', views.mark_sent, name='mark_sent'),
    path('bio/<str:token>/', views.public_bio_view, name='public_bio'),
    path('bio-history/', views.bio_history, name='bio_history'),
]
