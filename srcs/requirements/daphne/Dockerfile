# FROM python:3.12.6-alpine3.20

# WORKDIR /ft_transcendence

# # Copia o projeto para dentro do container
# COPY . /ft_transcendence

# # Garantindo que o script de entrada tenha permissões de execução
# RUN chmod +x /ft_transcendence/srcs/requirements/daphne/entrypoint.sh

# # Expondo a porta que o Daphne vai utilizar
# EXPOSE 8001

# # Criando um ambiente virtual e instalando as dependências
# RUN pip install --upgrade pip && \
#     pip install -r /ft_transcendence/srcs/requirements/daphne/requirements.txt

# # Definindo a variável de ambiente PYTHONPATH
# ENV PYTHONPATH="${PYTHONPATH}:/ft_transcendence/srcs/app"

# # Executa o script de inicialização do Daphne
# CMD ["/ft_transcendence/srcs/requirements/daphne/entrypoint.sh"]

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
COPY ./srcs/requirements/daphne/scripts /scripts

# Entra na pasta ft_transcendence no container
WORKDIR /ft_transcendence

# Exponha a porta que os servidores vão usar
EXPOSE 8001

RUN python -m venv /venv && \
  /venv/bin/pip install --upgrade pip && \
  /venv/bin/pip install -r /ft_transcendence/requirements.txt 

# Adiciona a pasta scripts e venv/bin 
# no $PATH do container.
ENV PATH="/scripts:/venv/bin:$PATH"

# Executa o arquivo scripts/commands.sh
CMD ["/scripts/entrypoint.sh"]

# Comando para iniciar os servidores
# CMD ["sh", "-c", "gunicorn ft_transcendence.wsgi:application --bind 0.0.0.0:8000 & daphne ft_transcendence.asgi:application --bind 0.0.0.0 --port 8001"]
