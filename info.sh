#!/bin/sh

POSTGRES_DB="transcendence"
POSTGRES_PASSWORD="transcendence"
POSTGRES_HOST="postgres"
POSTGRES_PORT="5432"

PGADMIN_DEFAULT_EMAIL="admin@admin.com"
PGADMIN_DEFAULT_PASSWORD="root"

GF_SECURITY_ADMIN_USER="grafana"
GF_SECURITY_ADMIN_PASSWORD="5432"

MINIO_ROOT_USER="minio"
MINIO_ROOT_PASSWORD="87654321"

echo "app:      http://localhost"
echo "          https://localhost"
# echo "Portainer:    https://localhost:9443"
echo "pgAdmin:  http://localhost:5050"
echo "          Login: ${PGADMIN_DEFAULT_EMAIL}"
echo "          Password: ${PGADMIN_DEFAULT_PASSWORD}"
echo "          Database: ${POSTGRES_DB}"
echo "          Server: ${POSTGRES_HOST}"
echo "          Port: ${POSTGRES_PORT}"
echo "          Password: ${POSTGRES_PASSWORD}"
echo "minIO:    http://localhost:9001"
echo "          Username: ${MINIO_ROOT_USER}"
echo "          Password: ${MINIO_ROOT_PASSWORD}"
echo "Prometheus:   http://localhost:9090"
echo "Grafana:  http://localhost:3000"
echo "          Username: ${GF_SECURITY_ADMIN_USER}"
echo "          Password: ${GF_SECURITY_ADMIN_PASSWORD}"
