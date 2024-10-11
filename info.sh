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

# Exibe informações sobre os serviços disponíveis

echo -e "\n ##### app #####"
echo -e "WSGI App (Gunicorn + Nginx - static files):"
echo -e "   - HTTP:       http://localhost"
echo -e "   - HTTPS:      https://localhost"
echo -e
echo -e "ASGI App (Consumer Service):"
echo -e "   - HTTP:       http://localhost:8001"
echo -e "   - Test Endpoint: http://localhost:8001/test/"
echo -e
echo -e "ASGI App (WebSocket):"
echo -e "   - WebSocket:  http://localhost/chat"
echo -e "   - WebSocket (HTTPS): https://localhost/chat/"

# echo -e "Portainer:    https://localhost:9443"

echo -e "\n ##### pgAdmin #####"
echo -e "   - URL:      http://localhost:5050"
echo -e "   - Login:    ${PGADMIN_DEFAULT_EMAIL}"
echo -e "   - Password: ${PGADMIN_DEFAULT_PASSWORD}"
echo -e "   - Database: ${POSTGRES_DB}"
echo -e "   - Server:   ${POSTGRES_HOST}"
echo -e "   - Port:     ${POSTGRES_PORT}"
echo -e "   - Password: ${POSTGRES_PASSWORD}"

echo -e "\n ##### minIO #####"
echo -e "   - URL:      http://localhost:9001"
echo -e "   - Username: ${MINIO_ROOT_USER}"
echo -e "   - Password: ${MINIO_ROOT_PASSWORD}"

echo -e "\n ##### selenium #####"
echo -e "   - URL:      http://localhost:4444"

echo -e "\n ##### prometheus #####"
echo -e "   - URL:      http://localhost:9090"

echo -e "\n ##### grafana #####"
echo -e "   - URL:      http://localhost:3000"
echo -e "   - Username: ${GF_SECURITY_ADMIN_USER}"
echo -e "   - Password: ${GF_SECURITY_ADMIN_PASSWORD}"

echo -e "\n ##### portainer #####"
echo -e "   - URL:      http://localhost:9000\n"