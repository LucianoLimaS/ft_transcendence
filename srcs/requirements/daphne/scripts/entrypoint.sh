#!/bin/sh

# O shell irá encerrar a execução do script quando um comando falhar
set -e

# Inicia o daphne
if [ "$DEBUG" = "0" ]; then
  echo "🔧 DEBUG=False detectado. Iniciando o servidor de desenvolvimento do Django..."
  exec daphne -p 8001 -b 0.0.0.0 a_core.asgi:application
fi

# echo "🔧 Iniciando o Daphne..."
# exec daphne -p 8001 -b 0.0.0.0 a_core.asgi:application
