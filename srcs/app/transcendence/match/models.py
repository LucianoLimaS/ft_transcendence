from django.db import models
from django.utils.translation import gettext_lazy as _
from a_users.models import User
from tournaments.models import Tournaments

class Match(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('ongoing', 'Ongoing'),
        ('finished', 'Finished'),
    ]

    player_1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='matches_as_player1')
    player_2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='matches_as_player2')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    initial_lifes = models.IntegerField(default=3)
    player1_lifes = models.IntegerField(default=3)
    player2_lifes = models.IntegerField(default=3)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(null=True, blank=True)
    result = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"Match between {self.player_1.username} and {self.player_2.username}"

class UserMatch(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    match = models.ForeignKey(Match, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} plays in match {self.match.id}"
    
class TournamentMatch(models.Model):
    tournament = models.ForeignKey(Tournaments, on_delete=models.CASCADE)
    match = models.ForeignKey(Match, on_delete=models.CASCADE)

    def __str__(self):
        return f"Match {self.match.id} in Tournament {self.tournament.name}"