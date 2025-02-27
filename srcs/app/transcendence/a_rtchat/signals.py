# apps/chat/signals.py
from django.db.models.signals import post_migrate
from django.dispatch import receiver
from .models import *

@receiver(post_migrate)
def create_default_chat(sender, **kwargs):
    print("verificando se os chats publicos e online-status existem")
    if sender.name == 'a_rtchat':
        # Verifique se o chat padrão já existe
        if not ChatGroup.objects.filter(group_name='public-chat').exists():
            print("Criando chat publico")
            ChatGroup.objects.create(group_name='public-chat')
        if not ChatGroup.objects.filter(group_name='online-status').exists():
            print("Criando chat de status online")
            ChatGroup.objects.create(group_name='online-status')

