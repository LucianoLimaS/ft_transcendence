FROM grafana/grafana:main-ubuntu

# Copia os arquivos de provisionamento
COPY srcs/requirements/grafana/provisioning/dashboards /etc/grafana/provisioning/dashboards
COPY srcs/requirements/grafana/provisioning/datasources /etc/grafana/provisioning/datasources
COPY srcs/requirements/grafana/dashboards /etc/grafana/dashboards

# Define permissões para evitar erros
USER root

# Ajusta as permissões para o usuário grafana existente
RUN chown -R grafana:root /etc/grafana/provisioning /etc/grafana/dashboards
RUN chmod -R 755 /etc/grafana/provisioning /etc/grafana/dashboards

# Volta para o usuário grafana
USER grafana