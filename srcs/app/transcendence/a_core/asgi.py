"""
ASGI config for a_core project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""

import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter, ChannelNameRouter
from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'a_core.settings')
django_asgi_app = get_asgi_application()

import a_rtchat.routing
import match.routing
from pong.routing import channel_routing, ws_pong_application

application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": AllowedHostsOriginValidator(
        AuthMiddlewareStack(
            URLRouter(
                a_rtchat.routing.websocket_urlpatterns + match.routing.websocket_urlpatterns + ws_pong_application
            )
        )
    ),
    "channel": ChannelNameRouter(channel_routing),
})