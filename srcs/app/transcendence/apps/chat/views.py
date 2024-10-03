# srcs/app/transcendence/apps/chat/views.py
from django.shortcuts import render

def chat_index(request):  # O nome da função deve ser 'chat_index'
    return render(request, 'chat/index.html')
