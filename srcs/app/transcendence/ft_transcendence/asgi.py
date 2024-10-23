# asgi.py
import os
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.urls import path
from django.core.asgi import get_asgi_application
from transcendence.apps.chat.routing import websocket_urlpatterns
from transcendence.apps.chat.consumers import MyAsyncHttpConsumer  # Importa o novo consumidor
from channels.security.websocket import AllowedHostsOriginValidator

# Configuração do ambiente para o Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ft_transcendence.settings')

# Inicializa a aplicação ASGI do Django
application = get_asgi_application()

# Adicionando as rotas HTTP
http_urlpatterns = [
    path('', MyAsyncHttpConsumer.as_asgi(), name='home_view'),  # Rota para a raiz
    path('test/', MyAsyncHttpConsumer.as_asgi(), name='test_view'),  # Rota HTTP correta
]

# Definindo a aplicação ASGI
application = ProtocolTypeRouter({
    "http": URLRouter(http_urlpatterns),  # Usando URLRouter para rotas HTTP
    "websocket": AllowedHostsOriginValidator(  # Proteção contra ataques
        AuthMiddlewareStack(
            URLRouter(websocket_urlpatterns)  # Usando URLRouter para WebSocket
        )
    ),
})
