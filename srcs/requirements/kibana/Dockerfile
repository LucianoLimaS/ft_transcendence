FROM docker.elastic.co/kibana/kibana:8.17.2

# Copia o script para gerar certificados
COPY ./srcs/requirements/kibana/scripts/generate-certs.sh /usr/local/bin/generate-certs.sh

# Copia o arquivo de configuração do Kibana
COPY ./srcs/requirements/kibana/config/kibana.yml /usr/share/kibana/config/kibana.yml

USER root

# Adiciona o usuário kibana ao grupo compartilhado (certs_group)
RUN groupadd -r certs_group \
    && usermod -aG certs_group kibana

# Define permissões de execução para o script e arquivos de configuração
RUN chmod +x /usr/local/bin/generate-certs.sh \
    && chown kibana:certs_group /usr/local/bin/generate-certs.sh \
    && chown kibana:certs_group /usr/share/kibana/config/kibana.yml \
    # Certifica-se de que o diretório de certificados tem permissões corretas
    && mkdir -p /usr/share/kibana/config/certs/ca \
    && chown -R kibana:certs_group /usr/share/kibana/config/certs \
    && chmod -R 750 /usr/share/kibana/config/certs

USER kibana

# Define o entrypoint para gerar certificados e iniciar o Kibana
ENTRYPOINT ["/bin/bash", "-c", "generate-certs.sh"]