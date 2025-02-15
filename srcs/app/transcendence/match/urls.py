from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('pong/<int:game_id>/', views.pong, name='pong'),
    path('pong_local/', views.pongLocal, name='pong_local'),

    # Rotas do Torneio
    path('tournaments/', views.tournament_list, name='tournament_list'),
    path('tournaments/<int:tournament_id>/', views.tournament_detail, name='tournament_detail'),
]
