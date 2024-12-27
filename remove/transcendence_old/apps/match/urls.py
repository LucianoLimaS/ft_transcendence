# srcs/app/transcendence/apps/chat/urls.py
from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('pong/', views.pong, name='pong'),
    path('pong_local/', views.pongLocal, name='pong_sp'),
]
