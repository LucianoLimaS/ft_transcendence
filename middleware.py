from channels.db import database_sync_to_async
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth import get_user_model
from channels.middleware import BaseMiddleware
from django.contrib.sessions.models import Session
import logging

# Configuração de logs
logger = logging.getLogger(__name__)

# Obtendo o modelo de usuário globalmente
User = get_user_model()

class SessionAuthMiddleware(BaseMiddleware):
    """
    Middleware para autenticação de WebSocket via sessão.
    A autenticação é baseada no cookie de sessão.
    """

    async def __call__(self, scope, receive, send):
        # Recupera o usuário autenticado e o adiciona ao escopo
        scope['user'] = await self.get_user_from_scope(scope)
        # Passa o controle para a próxima camada de middleware
        return await super().__call__(scope, receive, send)

    @database_sync_to_async
    def get_user_from_scope(self, scope):
        """
        Retorna o usuário autenticado ou AnonymousUser com base na sessão.
        """
        # Verifica se os cookies estão disponíveis no escopo
        cookies = scope.get('cookies', {})
        if not cookies:
            logger.warning("Nenhum cookie encontrado no escopo do WebSocket.")
            return AnonymousUser()

        # Obtém o sessionid a partir dos cookies
        sessionid = cookies.get('sessionid')
        if not sessionid:
            logger.warning("Cookie 'sessionid' não encontrado.")
            return AnonymousUser()

        try:
            # Busca a sessão e decodifica os dados para obter o ID do usuário
            session = Session.objects.get(session_key=sessionid)
            user_id = session.get_decoded().get('_auth_user_id')

            if not user_id:
                logger.warning("ID do usuário não encontrado na sessão.")
                return AnonymousUser()

            # Busca o usuário pelo ID
            user = User.objects.get(id=user_id)
            return user

        except Session.DoesNotExist:
            logger.error(f"Sessão com sessionid '{sessionid}' não encontrada.")
        except User.DoesNotExist:
            logger.error(f"Usuário com ID '{user_id}' não encontrado.")
        except Exception as e:
            logger.exception(f"Erro inesperado ao recuperar o usuário: {e}")

        # Retorna AnonymousUser como fallback
        return AnonymousUser()
