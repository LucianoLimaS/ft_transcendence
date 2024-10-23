from django.apps import AppConfig


class ChatConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.chat'

    def ready(self):
        import apps.chat.signals  # Conecte o sinal de criação de chat padrão