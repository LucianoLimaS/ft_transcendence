from django.apps import AppConfig

class ARtchatConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'a_rtchat'

    def ready(self):
        import a_rtchat.signals  # Conecte o sinal de criação de chat padrão