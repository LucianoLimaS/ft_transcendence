#!/bin/sh

# O shell irá encerrar a execução do script quando um comando falhar
set -e

while ! nc -z $POSTGRES_HOST $POSTGRES_PORT; do
  echo "🟡 Waiting for Postgres Database Startup ($POSTGRES_HOST $POSTGRES_PORT) ..."
  sleep 2
done

echo "✅ Postgres Database Started Successfully ($POSTGRES_HOST:$POSTGRES_PORT)"

# Executa as migrações do Django
python manage.py migrate --noinput

# Inicia o Django em background
python manage.py runserver 0.0.0.0:8001 &

# Mantém o container rodando com um shell interativo
# Se você quer um loop infinito em vez de um shell interativo para manter o container vivo:
while true; do
  sleep 1000
done