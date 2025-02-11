FROM elasticsearch:8.17.0

COPY ./srcs/requirements/elasticsearch/elasticsearch.yml /usr/share/elasticsearch/config/
COPY ./srcs/requirements/certs/cert.pem /usr/share/elasticsearch/config/certs/
COPY ./srcs/requirements/certs/key.pem /usr/share/elasticsearch/config/certs/

USER root
RUN chown -R elasticsearch:elasticsearch /usr/share/elasticsearch/config \
    && chown -R elasticsearch:elasticsearch /usr/share/elasticsearch/data

USER elasticsearch

EXPOSE 9200

CMD ["bin/elasticsearch"]