#!/bin/sh

# O shell irá encerrar a execução do script quando um comando falhar
set -e

# Inicia o daphne
exec daphne -p 8001 -b 0.0.0.0 ft_transcendence.asgi:application
