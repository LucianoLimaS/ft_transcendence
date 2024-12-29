# srcs/app/transcendence/apps/chat/routing.py
from django.urls import path
from . import consumers

# Roteamento para WebSocket e HTTP
websocket_urlpatterns = [
    path('ws/pong/', consumers.PongConsumer.as_asgi()),  # Defina a rota desejada para o WebSocket
]