FROM python:3.12.6-alpine3.20

# Copia o projeto para dentro do container
COPY . /ft_transcendence

# Definindo o diretório de trabalho
WORKDIR /ft_transcendence/srcs/requirements/daphne

# Expondo a porta que o Daphne vai utilizar
EXPOSE 8001

# Criando um ambiente virtual e instalando as dependências
RUN python -m venv /venv && \
  /venv/bin/pip install --upgrade pip && \
  /venv/bin/pip install -r requirements.txt 

# Adiciona a pasta venv/bin no $PATH do container
ENV PATH="/venv/bin:$PATH"

ENV PYTHONPATH="${PYTHONPATH}:/ft_transcendence/srcs/app"

# Definindo o diretório de trabalho
WORKDIR /ft_transcendence/srcs/app/transcendence

# Executa o script de inicialização do Daphne
CMD ["/bin/sh", "-c", "source /venv/bin/activate && exec /ft_transcendence/srcs/requirements/daphne/entrypoint.sh"]