FROM kibana:8.17.0

COPY ./srcs/requirements/kibana/kibana.yml /usr/share/kibana/config/
COPY ./srcs/requirements/kibana/node.options /etc/kibana/node.options
COPY ./srcs/requirements/certs/cert.pem /usr/share/kibana/config/certs/
COPY ./srcs/requirements/certs/key.pem /usr/share/kibana/config/certs/

USER root

RUN chown -R kibana:kibana /usr/share/kibana/config/

USER kibana

EXPOSE 5601

CMD ["bin/kibana"]