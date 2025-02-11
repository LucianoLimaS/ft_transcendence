from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path('ws/pong/', consumers.PongConsumer.as_asgi()),  # WebSocket para Pong
    path('ws/tournaments/<int:tournament_id>/', consumers.TournamentConsumer.as_asgi()),
]