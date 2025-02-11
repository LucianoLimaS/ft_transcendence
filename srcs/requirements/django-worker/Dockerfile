# # Multistage with final build not including poetry
# FROM python:3.12.1-bullseye AS build

# # Install dependencies and setup env
# RUN curl -sSL https://install.python-poetry.org | python3 -
# ENV PATH="/root/.local/bin:$PATH"

# WORKDIR /build

# COPY ./pyproject.toml ./poetry.lock /build/

# # add poetry's export plugin
# RUN poetry self add poetry-plugin-export
# RUN poetry export -f requirements.txt --without-hashes -o ./requirements.txt
# RUN poetry export -f constraints.txt --without-hashes -o ./constraints.txt

# # final stage
# FROM python:3.12.1-bullseye AS image

# RUN apt-get update && apt-get install -y \
# 	curl \
# 	build-essential \
# 	libpq-dev \
# 	gettext

# WORKDIR /app

# COPY --from=build /build/requirements.txt /build/constraints.txt ./

# RUN pip install --no-cache-dir -r requirements.txt -c constraints.txt
# RUN pip install --no-cache-dir 'Twisted[tls,http2]'

# WORKDIR /app/ft_transcendence

# COPY ./ft_transcendence/ .

# COPY ./docker/django-worker/entrypoint.sh ./

# RUN chmod +x ./entrypoint.sh

# ENTRYPOINT ["./entrypoint.sh"]

FROM python:3.12.6-alpine3.20

# Essa variável de ambiente é usada para controlar se o Python deve 
# gravar arquivos de bytecode (.pyc) no disco. 1 = Não, 0 = Sim
ENV PYTHONDONTWRITEBYTECODE 1

# Define que a saída do Python será exibida imediatamente no console ou em 
# outros dispositivos de saída, sem ser armazenada em buffer.
# Em resumo, você verá os outputs do Python em tempo real.
ENV PYTHONUNBUFFERED 1

# Copia a pasta "ft_transcendence" e "scripts" para dentro do container.
COPY ./srcs/app/transcendence /ft_transcendence
COPY ./srcs/requirements/django-worker/scripts /scripts

# Entra na pasta ft_transcendence no container
WORKDIR /ft_transcendence

RUN python -m venv /venv && \
  /venv/bin/pip install --upgrade pip && \
  /venv/bin/pip install -r /ft_transcendence/requirements.txt && \
  chmod +x /scripts/entrypoint.sh

# Adiciona a pasta scripts e venv/bin 
# no $PATH do container.
ENV PATH="/scripts:/venv/bin:$PATH"

# Executa o arquivo scripts/commands.sh
CMD ["/scripts/entrypoint.sh"]

# Comando para iniciar os servidores
# CMD ["sh", "-c", "gunicorn ft_transcendence.wsgi:application --bind 0.0.0.0:8000 & daphne ft_transcendence.asgi:application --bind 0.0.0.0 --port 8001"]
