#!/bin/bash
set -e

USER=${ELASTICSEARCH_USERNAME}
PASSWD=${ELASTICSEARCH_PASSWORD}

if ! /usr/share/elasticsearch/bin/elasticsearch-users list | grep -q "$USER"; then
    /usr/share/elasticsearch/bin/elasticsearch-users useradd $USER -p $PASSWD -r superuser
fi

CERT_DIR="/usr/share/elasticsearch/config/certs"

# Cria o diretório de certificados se não existir
mkdir -p "$CERT_DIR"

# Cria a CA e os certificados do Elasticsearch se não existirem
if [ ! -f "$CERT_DIR/ca.zip" ]; then
    echo "Criando CA..."
    bin/elasticsearch-certutil ca --silent --pem -out "$CERT_DIR/ca.zip"
    unzip "$CERT_DIR/ca.zip" -d "$CERT_DIR"
fi

# Cria os certificados do Elasticsearch se não existirem
if [ ! -f "$CERT_DIR/certs.zip" ]; then
    echo "Criando certificados para o Elasticsearch..."
    echo -ne \
    "instances:\n"\
    "  - name: es01\n"\
    "    dns:\n"\
    "      - es01\n"\
    "      - localhost\n"\
    "      - elasticsearch\n"\
    "    ip:\n"\
    "      - 127.0.0.1\n"\
    "      - 172.18.0.3\n"\
    > "$CERT_DIR/instances.yml"
    bin/elasticsearch-certutil cert --silent --pem -out "$CERT_DIR/certs.zip" --in "$CERT_DIR/instances.yml" --ca-cert "$CERT_DIR/ca/ca.crt" --ca-key "$CERT_DIR/ca/ca.key"
    unzip "$CERT_DIR/certs.zip" -d "$CERT_DIR"
fi

# Remove os arquivos .zip após a descompactação
rm -f "$CERT_DIR/ca.zip" "$CERT_DIR/certs.zip"
echo "Arquivos .zip removidos."

# Espera o Kibana gerar e colocar seus certificados antes de iniciar o Elasticsearch
echo "Aguardando o Kibana gerar seus certificados..."
until [ -f "$CERT_DIR/kibana.crt" ] && [ -f "$CERT_DIR/kibana.key" ]; do
  echo "Aguardando certificados do Kibana..."
  sleep 5
done

# Inicia o Elasticsearch com os certificados gerados
echo "Iniciando o Elasticsearch com os certificados..."
/usr/share/elasticsearch/bin/elasticsearch
