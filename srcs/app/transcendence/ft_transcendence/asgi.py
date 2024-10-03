import os
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.urls import path
from django.core.asgi import get_asgi_application
from apps.chat.routing import websocket_urlpatterns
from transcendence.apps.chat.consumers import SimpleHtmlConsumer  # Consumer para teste

# Configuração do ambiente para o Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ft_transcendence.settings')

# Inicializa a aplicação ASGI do Django
django_asgi_app = get_asgi_application()

# Adicionando a rota de teste HTTP
http_urlpatterns = [
    path('test/', SimpleHtmlConsumer.as_asgi()),  # Rota de teste
]

# Definindo a aplicação ASGI
application = ProtocolTypeRouter({
    "http": URLRouter(http_urlpatterns),  # Usando URLRouter para as rotas HTTP
    "websocket": AuthMiddlewareStack(
        URLRouter(
            websocket_urlpatterns  # Usando o roteamento definido para WebSocket
        )
    ),
})
