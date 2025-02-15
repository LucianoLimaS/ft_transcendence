#!/bin/bash

# Nome do arquivo .env
ENV_FILE="srcs/.env"

# Verifica se o arquivo já existe
if [ -f "$ENV_FILE" ]; then
    echo "🟡 .env file already exists."
    exit 0
fi

cat <<EOL > "$ENV_FILE"
SECRET_KEY="django-insecure-hy0f)6#-mkp1kq9+4o2dh!(uv=oa07yy&eaamu*y@6(di22rm("

DJANGO_SETTINGS_MODULE=a_core.settings

# 0 False, 1 True
DEBUG="0"

#setup windows desktop environment
WINDOWS="0"

# Comma Separated values
ALLOWED_HOSTS="transcendence, 127.0.0.1, localhost, app, *"
CSRF_TRUSTED_ORIGINS="https://localhost, https://127.0.0.1"

DB_ENGINE="django_prometheus.db.backends.postgresql"
POSTGRES_DB="transcendence"
POSTGRES_USER="transcendence"
POSTGRES_PASSWORD="transcendence"
POSTGRES_HOST="postgres"
PG_HOST="postgres"
POSTGRES_PORT="5432"
DATA_SOURCE_NAME="postgresql://:@:/?sslmode=disable"
TZ="America/Sao_Paulo"

PGADMIN_DEFAULT_EMAIL="admin@admin.com"
PGADMIN_DEFAULT_PASSWORD="root"

GF_SECURITY_ADMIN_USER="grafana"
GF_SECURITY_ADMIN_PASSWORD="5432"
GF_PATHS_PROVISIONING=/etc/grafana/provisioning

MINIO_ROOT_USER="minio"
MINIO_ROOT_PASSWORD="87654321"
MINIO_BUCKET="transcendence"
MINIO_ENDPOINT="minio:9000"
MINIO_EXTERNAL_ENDPOINT="http://localhost:9002"

EMAIL_API_KEY="Pegar no discord"
DEFAULT_FROM_EMAIL="ft_transcendence@gmx.com"

REDIS_HOST="redis"
REDIS_PORT="6379"
REDIS_ADDR="redis:6379"

EOL

echo "✅ .env file created successfully."
