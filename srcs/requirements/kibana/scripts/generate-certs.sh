#!/bin/bash
set -e

CERT_DIR="/usr/share/kibana/config/certs"
CA_CERT="/usr/share/kibana/config/certs/ca/ca.crt"

# Aguardar o Elasticsearch gerar os certificados
echo "Aguardando Elasticsearch gerar os certificados..."
until [ -f "$CERT_DIR/es01/es01.crt" ]; do
  echo "Aguardando os certificados da CA e es01..."
  sleep 5  # Aguarda 5 segundos antes de verificar novamente
done

# Gerando o certificado e a chave privada para o Kibana
echo "Certificado da CA encontrado! Gerando certificado e chave privada para o Kibana..."
openssl req -new -newkey rsa:2048 -nodes -keyout "$CERT_DIR/kibana.key" -out "$CERT_DIR/kibana.csr" -subj "/CN=kibana"
openssl x509 -req -in "$CERT_DIR/kibana.csr" -CA "$CA_CERT" -CAkey "$CERT_DIR/ca/ca.key" -CAcreateserial -out "$CERT_DIR/kibana.crt" -days 365

# Remove o arquivo .csr (não é mais necessário)
rm -f "$CERT_DIR/kibana.csr"

echo "Certificado e chave privada do Kibana gerados com sucesso!"

# Espera até que o Elasticsearch tenha inicializado corretamente
echo "Aguardando o Elasticsearch iniciar..."
until curl -s -u "${ELASTICSEARCH_USERNAME}:${ELASTICSEARCH_PASSWORD}" https://elasticsearch:9200; do  echo "Aguardando Elasticsearch..."
  sleep 15
done

# Criando o usuário no Elasticsearch para o Kibana
echo "Criando o usuário no Elasticsearch para o Kibana..."
curl -k -u "${ELASTICSEARCH_USERNAME}:${ELASTICSEARCH_PASSWORD}" -X POST "https://elasticsearch:9200/_security/user/${ELASTICSEARCH_USERNAME}" -H 'Content-Type: application/json' -d '{
  "password": "'"${ELASTICSEARCH_PASSWORD}"'",
  "roles": ["superuser"],
  "full_name": "Kibana User",
  "email": "kibana@example.com"
}'

# Aqui inicia o Kibana após garantir que o Elasticsearch está pronto e os certificados foram gerados
echo "Iniciando o Kibana com os certificados gerados..."
/usr/share/kibana/bin/kibana
