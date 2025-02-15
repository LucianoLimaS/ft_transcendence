#!/bin/sh

echo "Iniciando entrypoint.sh..."

# Função para verificar se o MinIO está ativo
isAlive() {
    echo "Verificando se o MinIO está ativo..."
    curl -sf http://127.0.0.1:9000/minio/health/live
}

# Inicia o MinIO em segundo plano
echo "Iniciando MinIO em segundo plano..."
minio server /data --console-address ":9001" --quiet &
echo $! > /tmp/minio.pid

# Aguarda até que o MinIO esteja ativo
echo "Aguardando MinIO ficar ativo..."
while ! isAlive; do
    sleep 0.1
done

# Configura o cliente MinIO
echo "Configurando o cliente MinIO..."
mc alias set minio http://127.0.0.1:9000 $MINIO_ROOT_USER $MINIO_ROOT_PASSWORD

# Cria um bucket (se não existir)
echo "Criando bucket $MINIO_BUCKET..."
mc mb minio/$MINIO_BUCKET || true

# Torna o bucket público
echo "Tornando o bucket público..."
mc anonymous set public minio/$MINIO_BUCKET

# Para o MinIO
echo "Parando MinIO..."
kill -s INT $(cat /tmp/minio.pid) && rm /tmp/minio.pid

# Aguarda até que o MinIO seja parado
echo "Aguardando MinIO parar..."
while isAlive; do
    sleep 0.1
done

# Inicia o MinIO em primeiro plano
echo "Iniciando MinIO em primeiro plano..."
exec minio server /data --console-address ":9001"