# apps/chat/signals.py
from django.db.models.signals import post_migrate
from django.dispatch import receiver
from .models import Chat, Users

@receiver(post_migrate)
def create_default_chat(sender, **kwargs):
    if sender.name == 'apps.chat':
        # Verifique se o chat padrão já existe
        if not Chat.objects.filter(users__isnull=True).exists():
            # Crie um chat padrão
            default_chat = Chat.objects.create()
            print("Chat padrão criado com sucesso.")