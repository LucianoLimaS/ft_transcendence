#!/bin/bash

# Nome do arquivo .env
ENV_FILE="srcs/.env"

# Verifica se o arquivo já existe
if [ -f "$ENV_FILE" ]; then
    echo "🔴 .env file already exists."
    exit 1
fi

cat <<EOL > "$ENV_FILE"
SECRET_KEY="django-insecure-hy0f)6#-mkp1kq9+4o2dh!(uv=oa07yy&eaamu*y@6(di22rm("

# 0 False, 1 True
DEBUG="1"

# Comma Separated values
ALLOWED_HOSTS="transcendence, 127.0.0.1, localhost"

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

MINIO_ROOT_USER="minio"
MINIO_ROOT_PASSWORD="87654321"
MINIO_BUCKET="transcendence"

EMAIL_HOST="smtp.gmx.com"
EMAIL_HOST_USER="ft_transcendence@gmx.com"
EMAIL_HOST_PASSWORD="ft_transcendence!"
EMAIL_PORT="587"
EMAIL_USE_SSL="0"
EMAIL_USE_TLS="1"
DEFAULT_FROM_EMAIL="ft_transcendence@gmx.com"
EOL

echo "✅ .env file created successfully."
