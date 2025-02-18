#!/bin/sh

if [ -f ./srcs/.env ]; then
    export $(cat ./srcs/.env | xargs)
else
    echo "Arquivo .env não encontrado!"
    exit 1
fi

# Verificação para garantir que as variáveis foram carregadas corretamente
echo "POSTGRES_DB: ${POSTGRES_DB}"
echo "POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}"

# Carrega as variáveis de ambiente
POSTGRES_DB="${POSTGRES_DB}"
POSTGRES_PASSWORD="${POSTGRES_PASSWORD}"
POSTGRES_HOST="${POSTGRES_HOST}"
POSTGRES_PORT="${POSTGRES_PORT}"

PGADMIN_DEFAULT_EMAIL="${PGADMIN_DEFAULT_EMAIL}"
PGADMIN_DEFAULT_PASSWORD="${PGADMIN_DEFAULT_PASSWORD}"

GF_SECURITY_ADMIN_USER="${GF_SECURITY_ADMIN_USER}"
GF_SECURITY_ADMIN_PASSWORD="${GF_SECURITY_ADMIN_PASSWORD}"

MINIO_ROOT_USER="${MINIO_ROOT_USER}"
MINIO_ROOT_PASSWORD="${MINIO_ROOT_PASSWORD}"

ELASTICSEARCH_USERNAME="${ELASTICSEARCH_USERNAME}"
ELASTICSEARCH_PASSWORD="${ELASTICSEARCH_PASSWORD}"

# Exibe informações sobre os serviços disponíveis
echo -e "\n ##### app #####"
echo -e "   - http://localhost"

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

echo -e "\n ##### kibana #####"
echo -e "   - URL:      http://localhost:5601"
echo -e "   - Username: ${ELASTICSEARCH_USERNAME}"
echo -e "   - Password: ${ELASTICSEARCH_PASSWORD}"

echo -e "\n ##### portainer #####"
echo -e "   - URL:      http://localhost:9000\n"
