#!/bin/bash
if [ ! -d "/home/camuri/data" ]; then
        mkdir /home/camuri/data
        mkdir /home/camuri/data/app
        mkdir /home/camuri/data/grafana
        mkdir /home/camuri/data/minio
        mkdir /home/camuri/data/pgadmin
        mkdir /home/camuri/data/postgres
        mkdir /home/camuri/data/prometheus
        mkdir /home/camuri/data/selenium
        mkdir /home/camuri/data/nginx
        mkdir /home/camuri/data/staticfiles
        mkdir /home/camuri/data/portainer
        mkdir /home/camuri/data/redis
        mkdir /home/camuri/data/elasticsearch
        mkdir /home/camuri/data/es
        mkdir /home/camuri/data/kibana
        mkdir /home/camuri/data/logstash
        mkdir /home/camuri/data/filebeat
        mkdir /home/camuri/data/certs
        sudo chmod -R 777 /home/camuri/data
fi
