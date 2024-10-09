FROM postgres:latest

# Copiar os certificados SSL para o container
COPY ./srcs/requirements/certs/cert.pem /etc/ssl/certs/cert.pem
COPY ./srcs/requirements/certs/key.pem /etc/ssl/private/key.pem

# Definir as permissões adequadas para a chave privada
RUN chmod 600 /etc/ssl/private/key.pem && \
    chown postgres:postgres /etc/ssl/private/key.pem

# Usar um script de inicialização para configurar o SSL
RUN echo "#!/bin/bash \n \
    echo \"ssl = on\" >> /var/lib/postgresql/data/postgresql.conf && \
    echo \"ssl_cert_file = '/etc/ssl/certs/cert.pem'\" >> /var/lib/postgresql/data/postgresql.conf && \
    echo \"ssl_key_file = '/etc/ssl/private/key.pem'\" >> /var/lib/postgresql/data/postgresql.conf" > /docker-entrypoint-initdb.d/setup_ssl.sh

RUN chmod +x /docker-entrypoint-initdb.d/setup_ssl.sh

# Usar o comando padrão do PostgreSQL para iniciar o servidor
CMD ["postgres"]
