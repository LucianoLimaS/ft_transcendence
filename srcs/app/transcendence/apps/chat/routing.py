# srcs/app/transcendence/apps/chat/routing.py
from django.urls import path
from . import consumers

# Roteamento para WebSocket e HTTP
websocket_urlpatterns = [
    path('ws/chat/', consumers.ChatConsumer.as_asgi()),  # Defina a rota desejada para o WebSocket
]

http_urlpatterns = [
    path('test', consumers.MyAsyncHttpConsumer.as_asgi(), name='test_view'),  # Direciona para o consumidor
    path('', consumers.MyAsyncHttpConsumer.as_asgi(), name='home_view'),  # Direciona para o consumidor
]
