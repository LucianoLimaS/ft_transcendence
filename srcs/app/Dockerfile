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

# RUN executa comandos em um shell dentro do container para construir a imagem. 
# O resultado da execução do comando é armazenado no sistema de arquivos da 
# imagem como uma nova camada.
# Agrupar os comandos em um único RUN pode reduzir a quantidade de camadas da 
# imagem e torná-la mais eficiente.
RUN python -m venv /venv && \
  /venv/bin/pip install --upgrade pip && \
  /venv/bin/pip install -r /ft_transcendence/requirements.txt 

# Adiciona a pasta scripts e venv/bin 
# no $PATH do container.
ENV PATH="/scripts:/venv/bin:$PATH"

# Executa o arquivo scripts/commands.sh
CMD ["/scripts/commands.sh"]

# Comando para iniciar os servidores
# CMD ["sh", "-c", "gunicorn ft_transcendence.wsgi:application --bind 0.0.0.0:8000 & daphne ft_transcendence.asgi:application --bind 0.0.0.0 --port 8001"]
