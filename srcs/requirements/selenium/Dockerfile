FROM python:3.12.6-alpine3.20

# Instalar dependências do sistema e o Chrome
RUN apk add --no-cache \
    chromium \
    chromium-chromedriver \
    curl \
    && ln -s /usr/bin/chromium-browser /usr/bin/chrome

# Definir o diretório de trabalho
WORKDIR /usr/src/app

# Copiar o requirements.txt e instalar as dependências
COPY ./srcs/requirements/selenium/requirements.txt ./

# Criar um ambiente virtual e instalar as dependências
RUN python -m venv /venv && \
    /venv/bin/pip install --upgrade pip && \
    /venv/bin/pip install --no-cache-dir -r requirements.txt

# Copiar seu script de coleta de métricas para o contêiner
COPY ./srcs/requirements/selenium/custom_exporter.py ./
COPY ./srcs/requirements/selenium/wait_for_selenium.sh ./

# Tornar o script de espera executável
RUN chmod +x ./wait_for_selenium.sh

# Definir o comando para iniciar seu script usando o Python do ambiente virtual
CMD ["/bin/sh", "-c", "/usr/src/app/wait_for_selenium.sh"]
