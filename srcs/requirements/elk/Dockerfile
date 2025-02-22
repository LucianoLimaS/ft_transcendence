FROM elastic/filebeat:8.7.1

COPY ./srcs/requirements/elk/filebeat.yml /usr/share/filebeat/filebeat.yml

# Define permissões dentro do container
USER root
RUN chown root:root /usr/share/filebeat/filebeat.yml && \
    chmod 600 /usr/share/filebeat/filebeat.yml

# Define o script de entrada
# ENTRYPOINT ["/usr/share/filebeat/entrypoint.sh"]
CMD ["filebeat", "-e"]