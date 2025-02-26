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

DEBUG="0"

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

EMAIL_API_KEY="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"
DEFAULT_FROM_EMAIL="ft_transcendence@gmx.com"

REDIS_HOST="redis"
REDIS_PORT="6379"
REDIS_ADDR="redis:6379"

ES_JAVA_OPTS=-Xms512m -Xmx512m
ES_MEM_LIMIT=1073741824
KB_MEM_LIMIT=1073741824
LICENSE=basic
CLUSTER_NAME=es_cluster
ELASTIC_USER=elastic
ELASTIC_PASSWORD=must_be_string
ELASTIC_HOSTS=https://elasticsearch:9200

KIBANA_PASSWORD=must_be_string
ENCRYPTION_KEY=c34d38b3a14956121ff2170e5030b471551370178f43e5626eec58b04a30fae2

EOL

echo "✅ .env file created successfully."
