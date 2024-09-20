from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.users.models import Users
from apps.tournaments.models import Tournaments
from django.db.models.functions import Now

class Badge(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='badges/')

    def __str__(self):
        return self.name
    
class UserBadge(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    badge = models.ForeignKey(Badge, on_delete=models.CASCADE)
    date_awarded = models.DateTimeField(db_default=Now())

    def __str__(self):
        return f"{self.user.username} awarded {self.badge.name}"
    
class TournamentBadge(models.Model):
    badge = models.ForeignKey(Badge, on_delete=models.CASCADE)
    tournament = models.ForeignKey(Tournaments, on_delete=models.CASCADE)  # Definindo uma ForeignKey para o Tournament (criado abaixo)
    position = models.IntegerField()

    def __str__(self):
        return f"Badge {self.badge.name} for position {self.position} in {self.tournament.name}"