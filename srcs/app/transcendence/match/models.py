from django.db import models
from django.conf import settings
from django.utils import timezone


class Tournament(models.Model):
    name = models.CharField(max_length=200, default="Tournament")
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    size = models.PositiveSmallIntegerField(choices=[(2, '2 Players'), (4, '4 Players'), (8, '8 Players'), (16, '16 Players')], default=4)
    is_started = models.BooleanField(default=False)
    current_round = models.PositiveSmallIntegerField(default=1)

    def __str__(self):
        return f"{self.name} ({self.size} players) by {self.created_by.username}"

    @property
    def available_slots(self):
        return self.size - self.participants.count()

    @property
    def is_full(self):
        return self.available_slots == 0


class Participant(models.Model):
    tournament = models.ForeignKey(Tournament, related_name='participants', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    position = models.PositiveSmallIntegerField(default=0)
    wins = models.PositiveSmallIntegerField(default=0)

    class Meta:
        unique_together = ('tournament', 'user')
    def __str__(self):
        return f"{self.user.username} in {self.tournament.name} (position: {self.position})"