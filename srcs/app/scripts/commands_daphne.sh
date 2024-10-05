#!/bin/sh

# O shell irá encerrar a execução do script quando um comando falhar
set -e

# Verifica se o daphne está instalado
command -v daphne >/dev/null 2>&1 || { echo >&2 "Daphne não está instalado. Abandonando."; exit 1; }

# Imprime o diretório atual
echo "Diretório atual: $(pwd)"

# Inicia o daphne
exec daphne -p 8001 -b 0.0.0.0 ft_transcendence.asgi:application

# # Mantém o container rodando com um shell interativo
# # Se você quer um loop infinito em vez de um shell interativo para manter o container vivo:
# while true; do
#   sleep 1000
# done