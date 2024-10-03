# srcs/app/transcendence/apps/chat/routing.py
from django.urls import path
from . import consumers

# Importar o consumer para o HTML simples
from .consumers import SimpleHtmlConsumer

# Roteamento para WebSocket e HTTP
websocket_urlpatterns = [
    path('ws/chat/', consumers.ChatConsumer.as_asgi()),  # Defina a rota desejada para o WebSocket
]

http_urlpatterns = [
    path('test/', SimpleHtmlConsumer.as_asgi()),  # Rota para o HTML simples
]
