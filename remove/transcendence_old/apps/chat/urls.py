# srcs/app/transcendence/apps/chat/urls.py
from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('test/', views.chat_test, name='test'),  
    path('chat/', login_required(views.chat_index), name='chat'),
    path('send_message/', views.send_message, name='send_message'),
]
