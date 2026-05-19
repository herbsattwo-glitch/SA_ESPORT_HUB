from django.urls import path
from . import views

urlpatterns = [
    path('', views.league_list, name='league_list'),
    path('create/', views.league_create, name='league_create'),
    path('<int:pk>/', views.league_detail, name='league_detail'),
    path('<int:pk>/edit/', views.league_update, name='league_update'),
    path('<int:pk>/delete/', views.league_delete, name='league_delete'),
    path('<int:pk>/register/', views.league_register, name='league_register'),
    path('<int:league_pk>/match/', views.record_match, name='record_match'),
]