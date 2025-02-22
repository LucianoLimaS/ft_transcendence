#!/bin/sh

# Cores ANSI
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[1;36m'
NC='\033[0m' # Sem cor

if [ -f ./srcs/.env ]; then
    set -o allexport
    grep -v '^#' ./srcs/.env | grep -E '^[A-Z_]+=[^,]+$' | sed 's/\r//g' > /tmp/envfile
    . /tmp/envfile
    set +o allexport
else
    echo -e "${RED}[ERRO] Arquivo .env não encontrado!${NC}"
    exit 1
fi

echo -e "\n${CYAN}========== INFORMAÇÕES DO AMBIENTE ==========${NC}"

echo -e "\n${YELLOW}##### app #####${NC}"
echo -e "   - ${GREEN}http://localhost${NC}"

echo -e "\n${YELLOW}##### pgAdmin #####${NC}"
echo -e "   - URL:      ${GREEN}http://localhost:5050${NC}"
echo -e "   - Login:    ${GREEN}${PGADMIN_DEFAULT_EMAIL}${NC}"
echo -e "   - Password: ${GREEN}${PGADMIN_DEFAULT_PASSWORD}${NC}"
echo -e "   - Database: ${GREEN}${POSTGRES_DB}${NC}"
echo -e "   - Server:   ${GREEN}${POSTGRES_HOST}${NC}"
echo -e "   - Port:     ${GREEN}${POSTGRES_PORT}${NC}"
echo -e "   - Password: ${GREEN}${POSTGRES_PASSWORD}${NC}"

echo -e "\n${YELLOW}##### minIO #####${NC}"
echo -e "   - URL:      ${GREEN}http://localhost:9001${NC}"
echo -e "   - Username: ${GREEN}${MINIO_ROOT_USER}${NC}"
echo -e "   - Password: ${GREEN}${MINIO_ROOT_PASSWORD}${NC}"

echo -e "\n${YELLOW}##### selenium #####${NC}"
echo -e "   - URL:      ${GREEN}http://localhost:4444${NC}"

echo -e "\n${YELLOW}##### prometheus #####${NC}"
echo -e "   - URL:      ${GREEN}http://localhost:9090${NC}"

echo -e "\n${YELLOW}##### grafana #####${NC}"
echo -e "   - URL:      ${GREEN}http://localhost:3000${NC}"
echo -e "   - Username: ${GREEN}${GF_SECURITY_ADMIN_USER}${NC}"
echo -e "   - Password: ${GREEN}${GF_SECURITY_ADMIN_PASSWORD}${NC}"

echo -e "\n${YELLOW}##### kibana #####${NC}"
echo -e "   - URL:      ${GREEN}http://localhost:5601${NC}"
echo -e "   - Username: ${GREEN}${ELASTIC_USER}${NC}"
echo -e "   - Password: ${GREEN}${KIBANA_PASSWORD}${NC}"

echo -e "\n${YELLOW}##### portainer #####${NC}"
echo -e "   - URL:      ${GREEN}http://localhost:9000${NC}"

echo -e "\n${CYAN}========== FIM ==========${NC}\n"
