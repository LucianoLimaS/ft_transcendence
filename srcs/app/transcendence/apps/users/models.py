from django_prometheus.models import ExportModelOperationsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser

class Users(AbstractUser):
    description = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True, max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_login = models.DateTimeField(blank=True, null=True)
    user_status = models.CharField(max_length=50, default='Ativo')
    token = models.CharField(max_length=100, blank=True, null=True, default=None)
    token_expires = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.username
    
class Friendship(models.Model):
    user1 = models.ForeignKey(Users, related_name='friends1', on_delete=models.CASCADE)
    user2 = models.ForeignKey(Users, related_name='friends2', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user1.username} and {self.user2.username}"