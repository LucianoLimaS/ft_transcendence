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
COPY ./srcs/app/scripts /scripts

# Entra na pasta ft_transcendence no container
WORKDIR /ft_transcendence

# Exponha a porta que os servidores vão usar
EXPOSE 8000

RUN apk update && apk add gettext && \
  python -m venv /venv && \
  /venv/bin/pip install --upgrade pip && \
  /venv/bin/pip install -r /ft_transcendence/requirements.txt 

# Adiciona a pasta scripts e venv/bin 
# no $PATH do container.
ENV PATH="/scripts:/venv/bin:$PATH"

# Executa o arquivo scripts/commands.sh
CMD ["/scripts/commands.sh"]
