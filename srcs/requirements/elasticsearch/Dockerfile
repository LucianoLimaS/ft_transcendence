FROM docker.elastic.co/elasticsearch/elasticsearch:8.17.2

# Copia o script para gerar certificados
COPY ./srcs/requirements/elasticsearch/scripts/generate-certs.sh /usr/local/bin/generate-certs.sh
COPY ./srcs/requirements/elasticsearch/config/elasticsearch.yml /usr/share/elasticsearch/config/elasticsearch.yml

USER root

# Cria um grupo compartilhado e adiciona o usuário elasticsearch e kibana a ele
RUN groupadd -r certs_group \
    && usermod -aG certs_group elasticsearch \
    && mkdir -p /usr/share/elasticsearch/config/certs/ca \
    && chown -R elasticsearch:certs_group /usr/share/elasticsearch/config/certs \
    && chmod -R 750 /usr/share/elasticsearch/config/certs

# Verifica se o arquivo de configuração e script existem
RUN if [ ! -f /usr/share/elasticsearch/config/elasticsearch.yml ]; then echo "Config file not found!"; exit 1; fi \
    && if [ ! -f /usr/local/bin/generate-certs.sh ]; then echo "Cert script not found!"; exit 1; fi

# Define permissões de execução para o script e configurações
RUN chmod +x /usr/local/bin/generate-certs.sh \
    && chown elasticsearch:certs_group /usr/local/bin/generate-certs.sh \
    && chown elasticsearch:certs_group /usr/share/elasticsearch/config/elasticsearch.yml

USER elasticsearch

# Define o entrypoint para gerar certificados e iniciar o Elasticsearch
ENTRYPOINT ["/bin/bash", "-c", "generate-certs.sh"]
