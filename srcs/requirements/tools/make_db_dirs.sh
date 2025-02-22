#!/bin/bash
if [ ! -d "/home/${USER}/data" ]; then
        mkdir /home/${USER}/data
        mkdir /home/${USER}/data/app
        mkdir /home/${USER}/data/grafana
        mkdir /home/${USER}/data/minio
        mkdir /home/${USER}/data/pgadmin
        mkdir /home/${USER}/data/postgres
        mkdir /home/${USER}/data/prometheus
        mkdir /home/${USER}/data/selenium
        mkdir /home/${USER}/data/nginx
        mkdir /home/${USER}/data/staticfiles
        mkdir /home/${USER}/data/portainer
        mkdir /home/${USER}/data/redis
        mkdir /home/${USER}/data/elasticsearch
        mkdir /home/${USER}/data/es
        mkdir /home/${USER}/data/kibana
        mkdir /home/${USER}/data/logstash
        mkdir /home/${USER}/data/filebeat
        mkdir /home/${USER}/data/certs
        mkdir /home/${USER}/data/logs
        sudo chmod -R 777 /home/${USER}/data
fi
