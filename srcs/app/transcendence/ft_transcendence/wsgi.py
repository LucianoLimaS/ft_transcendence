import os
from django.core.wsgi import get_wsgi_application
from prometheus_client import make_wsgi_app, start_http_server

# Verifica o valor da variável DEBUG (0 para produção, 1 para desenvolvimento)
debug_mode = os.environ.get('DEBUG', '1')  # Default para '1' (desenvolvimento)

# Se DEBUG for 0 (produção), inicia o servidor Prometheus
if debug_mode == '0':
    start_http_server(8000)  # Inicia o servidor Prometheus na porta 8000

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ft_transcendence.settings')

# Criação da aplicação WSGI do Django
application = get_wsgi_application()

# Integra a aplicação Django com o Prometheus se estiver em modo de produção (DEBUG = 0)
if debug_mode == '0':
    application = make_wsgi_app(application)
