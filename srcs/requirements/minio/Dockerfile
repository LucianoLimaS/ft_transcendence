# Use a imagem base do Alpine
FROM python:3.12.6-alpine3.20

# Instala dependências necessárias
RUN apk add --no-cache curl

# Baixa e instala o MinIO Client (mc)
RUN wget -qO /usr/local/bin/mc https://dl.min.io/client/mc/release/linux-amd64/mc && \
    chmod +x /usr/local/bin/mc

# Baixa e instala o MinIO
RUN wget -qO /usr/local/bin/minio https://dl.min.io/server/minio/release/linux-amd64/minio && \
    chmod +x /usr/local/bin/minio

# Cria o diretório de dados do MinIO
RUN mkdir -p /data

# Copia o script de inicialização
COPY srcs/requirements/minio/scripts/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Portas expostas
EXPOSE 9000
EXPOSE 9001

# Comando de entrada
ENTRYPOINT ["/entrypoint.sh"]