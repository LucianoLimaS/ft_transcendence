# apps/chat/signals.py
from django.db.models.signals import post_migrate
from django.dispatch import receiver
from .models import *
from django.contrib.auth import get_user_model

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

@receiver(post_migrate)
def create_admin_user(sender, **kwargs):
    if sender.name == 'a_rtchat':
        User = get_user_model()
        if not User.objects.filter(username='admin').exists():
            print("Criando usuário admin")
            User.objects.create_superuser(
                username='admin',
                email='admin@admin.com',
                password='admin',
                first_name='Admin',
            )
        for i in range(1, 5):
            username = f'teste{i}'
            email = f'teste{i}@teste.com'
            if not User.objects.filter(username=username).exists():
                print(f"Criando usuário {username}")
                User.objects.create_user(
                    username=username,
                    email=email,
                    password='teste',
                    first_name=f'Teste {i}',
                )