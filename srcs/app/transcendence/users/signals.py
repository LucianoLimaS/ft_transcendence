from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save
#from allauth.account.models import EmailAddress
from django.contrib.auth.models import User
from .models import Profile, Friendship
from django.db.models.signals import post_migrate
from django.contrib.auth import get_user_model

@receiver(post_save, sender=User)       
def user_postsave(sender, instance, created, **kwargs):
    user = instance
    
    # add profile if user is created
    if created:
        Profile.objects.create(
            user = user,
        )        
        
@receiver(pre_save, sender=User)
def user_presave(sender, instance, **kwargs):
    if instance.username:
        instance.username = instance.username.lower()

@receiver(post_migrate)
def create_admin_user(sender, **kwargs):
        User = get_user_model()
        if not User.objects.filter(username='admin').exists():
            print("Criando usuário admin")
            User.objects.create_superuser(
                username='admin',
                email='admin@admin.com',
                password='admin',
                first_name='Admin',
            )
            print("\033[93mVerificando usuário Notificação do Sistema\033[0m")
        if not User.objects.filter(username='notificação do sistema').exists():
            print("\033[93mCriando usuário Notificação do Sistema\033[0m")
            system_user = User.objects.create_user(
                username='Notificação do Sistema',
                email='Notificação do Sistema@admin.com',
                password='admin',
                first_name='Admin',
            )
            print("\033[93mAtualizando Profile Notificação do Sistema\033[0m")
            Profile.objects.update_or_create(
                user=system_user,
                defaults={
                    'displayname': 'Notificação do Sistema',
                    'info': 'System notification user',
                    'user_status': 'Ativo'
                }
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

        admin_user = User.objects.get(username='admin')
        teste1_user = User.objects.get(username='teste1')
        teste2_user = User.objects.get(username='teste2')

        # Verifique se os usuários admin, teste1 e teste2 são amigos
        if (Friendship.objects.filter(from_user=admin_user, to_user=teste1_user, accepted=True).exists() or
            Friendship.objects.filter(from_user=teste1_user, to_user=admin_user, accepted=True).exists()) and \
        (Friendship.objects.filter(from_user=admin_user, to_user=teste2_user, accepted=True).exists() or
            Friendship.objects.filter(from_user=teste2_user, to_user=admin_user, accepted=True).exists()):
            print("Os usuários admin, teste1 e teste2 são amigos")
        else:
            print("Os usuários admin, teste1 e teste2 não são amigos")
            # Adicionar como amigos se não forem
            Friendship.objects.create(from_user=admin_user, to_user=teste1_user, accepted=True)
            Friendship.objects.create(from_user=admin_user, to_user=teste2_user, accepted=True)
            Friendship.objects.create(from_user=teste1_user, to_user=teste2_user, accepted=True)
            print("Os usuários admin, teste1 e teste2 foram adicionados como amigos")