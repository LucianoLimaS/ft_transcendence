from django.urls import path

from . import views

app_name = "pong"
urlpatterns = [
    path("play/", views.PongSelectGameMode.as_view(), name="selectmode"),
    path("enter/localtournament/", views.PongEnterLocalTournamentView.as_view(), name="pongenterlocaltournament"),
    path("enter/<str:game_mode>/", views.PongEnterView.as_view(), name="pongenter"),
    path("room/<int:room_id>/", views.PongRoomView.as_view(), name="pongroom"),
    path("localTournament/<int:num_players>/", views.PongLocalTournamentView.as_view(), name="pongenterlocaltournament"),
    path("localTournament/room/<int:room_id>/", views.PongRoomView.as_view(), name="pongroomLocal"),
    path(
        "tournament/<int:tournament_id>/",
        views.PongTournamentView.as_view(),
        name="pongtournament",
    ),
    path("user/stats/", views.UserStatsView.as_view(), name="user_stats"),
    path("user/history/", views.UserHistoryView.as_view(), name="user_history"),
    path("tournamenthistory/<int:user_id>/", views.UserTournamentHistoryView.as_view(), name="tournament_history"),
    path("matchhistory/<int:user_id>/", views.UserMatchHistoryView.as_view(), name="match_history"),
    path("config_nbr_players/", views.PongSelectNbrPlayers.as_view(), name="config_nbr_players"),
]
