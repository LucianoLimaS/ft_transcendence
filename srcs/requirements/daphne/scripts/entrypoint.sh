#!/bin/sh

# O shell irá encerrar a execução do script quando um comando falhar
set -e

# Inicia o daphne
echo "🔧 Iniciando o Daphne..."
exec daphne -p 8001 -b 0.0.0.0 a_core.asgi:application
