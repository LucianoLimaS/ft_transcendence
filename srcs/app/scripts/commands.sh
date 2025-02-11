#!/bin/sh

# O shell irá encerrar a execução do script quando um comando falhar
set -e

while ! nc -z $POSTGRES_HOST $POSTGRES_PORT; do
  echo "🟡 Waiting for Postgres Database Startup ($POSTGRES_HOST $POSTGRES_PORT) ..."
  sleep 2
done

echo "✅ Postgres Database Started Successfully ($POSTGRES_HOST:$POSTGRES_PORT)"

# Executa as migrações do Django
python manage.py makemigrations --noinput
python manage.py migrate --noinput
python manage.py compilemessages --verbosity=0
python manage.py collectstatic --noinput

# Ajusta as permissões para o diretório de arquivos estáticos
echo "🔧 Ajustando permissões para o diretório de arquivos estáticos..."
chown -R 1000:1000 ./staticfiles

# Verifica se DEBUG está definido como False
if [ "$DEBUG" = "1" ]; then
  echo "🔧 DEBUG=True detectado. Iniciando o servidor de desenvolvimento do Django..."
  exec python manage.py runserver 0.0.0.0:8000
else
  echo "🔧 DEBUG=False detectado. Mantendo container do app ativo..."
  tail -f /dev/null
fi

# echo "🔧 Iniciando o servidor de desenvolvimento do Django..."
# python manage.py runserver 0.0.0.0:8000
