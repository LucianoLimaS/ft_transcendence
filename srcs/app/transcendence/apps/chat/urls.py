# srcs/app/transcendence/apps/chat/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('chat/', views.chat_index, name='chat_index'),  # A função deve ser 'chat_index'
]
