#!/bin/sh

# O shell irá encerrar a execução do script quando um comando falhar
set -e

# Esperar até que o Selenium esteja disponível
while ! wget -q --spider http://localhost:4444/wd/hub/status; do
    echo "🟡 Waiting for Selenium Startup ..."
    sleep 2
done

echo "✅ Selenium Started Successfully"

# Iniciar o seu script de coleta de métricas
exec /venv/bin/python ./custom_exporter.py  # Altere para o nome do seu script se necessário
