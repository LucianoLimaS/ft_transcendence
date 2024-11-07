# asgi.py
import os
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.core.asgi import get_asgi_application
from django.urls import path
from apps.match.routing import websocket_urlpatterns as match_websocket
from apps.chat.routing import websocket_urlpatterns as chat_websocket
from apps.chat.consumers import MyAsyncHttpConsumer  # Importa o consumidor HTTP
from apps.match.consumers import PongConsumer  # Importa o consumidor do pong
from channels.security.websocket import AllowedHostsOriginValidator

# Configuração do ambiente para o Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ft_transcendence.settings')

# Inicializa a aplicação ASGI do Django
application = get_asgi_application()

# Adicionando as rotas HTTP
http_urlpatterns = [
    path('', MyAsyncHttpConsumer.as_asgi(), name='home_view'),  # Rota para a raiz
    path('test/', MyAsyncHttpConsumer.as_asgi(), name='test_view'),  # Rota HTTP
]

# Consolidando os WebSocket URL Patterns de todos os apps
websocket_urlpatterns = match_websocket + chat_websocket

# Definindo a aplicação ASGI
application = ProtocolTypeRouter({
    "http": URLRouter(http_urlpatterns),  # Rotas HTTP
    "websocket": AllowedHostsOriginValidator(  # Proteção contra ataques
        AuthMiddlewareStack(
            URLRouter(websocket_urlpatterns)  # URLRouter para rotas WebSocket consolidadas
        )
    ),
})
