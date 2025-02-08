from enum import Enum

from django.contrib.auth import get_user_model
from django.db import models


class GameMode(Enum):
    LOCAL = "local"
    ONLINE = "online"
    TOURNAMENT = "tournament"
    LOCALTOURNAMENT = "local_tournament"

    @classmethod
    def choices(cls):
        return [(gameMode.value, gameMode.name.capitalize()) for gameMode in cls]

    @classmethod
    def as_dict(cls):
        return {gameMode.name: gameMode.value for gameMode in cls}


class Tournament(models.Model):
    name = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)
    max_players = models.IntegerField(choices=[(4, "4 Players"), (8, "8 Players")])
    created_at = models.DateTimeField(auto_now_add=True)
    winner = models.ForeignKey(
        get_user_model(), on_delete=models.SET_NULL, null=True, blank=True, related_name="tournament_winner"
    )

    def __str__(self):
        return f"Tournament: {self.name}. Max_players: {self.max_players}"


class PongRoom(models.Model):
    # limitando o nome da sala para 50 caracteres pois channel_name é limitado a 100 caracteres
    name = models.CharField(max_length=50)
    game_mode = models.CharField(max_length=20, choices=GameMode.choices())
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    tournament = models.ForeignKey(
        Tournament,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="rooms",
    )

    def __str__(self):
        return f"PongRoom id: {self.id}. Room name: {self.name} - Game_mode: {self.game_mode}"


class Match(models.Model):
    room = models.ForeignKey(PongRoom, on_delete=models.CASCADE, related_name="matches")
    player1 = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name="player1",
        null=True,
        blank=True,
    )
    player2 = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name="player2",
        null=True,
        blank=True,
    )
    winner = models.ForeignKey(
        get_user_model(), on_delete=models.SET_NULL, null=True, blank=True
    )
    finished = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Match id: {self.id}. Room id: {self.room_id} - Player1_id: {self.player1_id} vs Player2_id: {self.player2_id}"


class TournamentParticipant(models.Model):
    tournament = models.ForeignKey(
        Tournament, on_delete=models.CASCADE, related_name="participants"
    )
    player = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    is_eliminated = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.player.username} in {self.tournament.name}"
