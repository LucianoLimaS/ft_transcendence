FROM python:3.12.6-alpine3.20

# Variáveis de ambiente
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Diretório de trabalho
WORKDIR /ft_transcendence

# Copiar todos os arquivos para o contêiner
COPY . /ft_transcendence

# Expor a porta do contêiner
EXPOSE 8005

# Instalar dependências do sistema, criar o ambiente virtual e instalar pacotes
RUN apk update && \
    apk add --no-cache gcc musl-dev libffi-dev && \
    python -m venv /venv && \
    /venv/bin/pip install --upgrade pip && \
    /venv/bin/pip install -r ./srcs/requirements/gunicorn/requirements.txt

# Adiciona a pasta scripts e venv/bin no PATH
ENV PATH="/scripts:/venv/bin:$PATH"

# Comando para rodar o Gunicorn
CMD ["/venv/bin/gunicorn", "a_core.wsgi:application", "--bind", "0.0.0.0:8005"]
