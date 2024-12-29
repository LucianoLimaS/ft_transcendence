from django.db import models
from django.utils.translation import gettext_lazy as _
from a_users.models import User

class Tournaments(models.Model):
    name = models.CharField(max_length=100)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    status = models.CharField(max_length=50)
    max_players = models.PositiveIntegerField()
    current_stage = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.name


class UserTournaments(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Use o modelo de usuário do Django
    tournament = models.ForeignKey(Tournaments, on_delete=models.CASCADE)
    registration_time = models.DateTimeField()

    def __str__(self):
        return f"{self.user.username} - {self.tournament.name}"


class TournamentStage(models.Model):
    tournament = models.ForeignKey(Tournaments, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    order = models.IntegerField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    stage_number = models.IntegerField()

    def __str__(self):
        return f"{self.name} - {self.tournament.name} - Stage {self.stage_number}"