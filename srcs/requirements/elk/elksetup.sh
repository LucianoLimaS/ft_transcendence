#!/bin/bash
# setup.sh

if [ -z "$ELASTIC_PASSWORD" ]; then
  echo "Set the ELASTIC_PASSWORD environment variable in the .env file"
  exit 1
elif [ -z "$KIBANA_PASSWORD" ]; then
  echo "Set the KIBANA_PASSWORD environment variable in the .env file"
  exit 1
fi

if [ ! -f /usr/share/elasticsearch/config/certs/ca.zip ]; then
  echo "Creating CA"
  bin/elasticsearch-certutil ca --silent --pem -out /usr/share/elasticsearch/config/certs/ca.zip
  unzip /usr/share/elasticsearch/config/certs/ca.zip -d /usr/share/elasticsearch/config/certs
fi

if [ ! -f /usr/share/elasticsearch/config/certs/certs.zip ]; then
  echo "Creating certs"
  echo -ne \
    "instances:\n"\
    "  - name: elasticsearch\n"\
    "    dns:\n"\
    "      - elasticsearch\n"\
    "      - localhost\n"\
    "    ip:\n"\
    "      - 127.0.0.1\n"\
    "  - name: kibana\n"\
    "    dns:\n"\
    "      - kibana\n"\
    "      - localhost\n"\
    "    ip:\n"\
    "      - 127.0.0.1\n"\
    > /usr/share/elasticsearch/config/certs/instances.yml
  bin/elasticsearch-certutil cert --silent --pem -out /usr/share/elasticsearch/config/certs/certs.zip --in /usr/share/elasticsearch/config/certs/instances.yml --ca-cert /usr/share/elasticsearch/config/certs/ca/ca.crt --ca-key /usr/share/elasticsearch/config/certs/ca/ca.key
  unzip /usr/share/elasticsearch/config/certs/certs.zip -d /usr/share/elasticsearch/config/certs
fi

echo "Setting file permissions"
chown -R root:root /usr/share/elasticsearch/config/certs
find /usr/share/elasticsearch/config/certs -type d -exec chmod 750 {} \;
find /usr/share/elasticsearch/config/certs -type f -exec chmod 640 {} \;

echo "Waiting for Elasticsearch availability"
until curl -s --cacert /usr/share/elasticsearch/config/certs/ca/ca.crt https://elasticsearch:9200 | grep -q "missing authentication credentials"; do sleep 30; done

echo "Setting kibana_system password"
until curl -s -X POST --cacert /usr/share/elasticsearch/config/certs/ca/ca.crt -u "elastic:${ELASTIC_PASSWORD}" -H "Content-Type: application/json" https://elasticsearch:9200/_security/user/kibana_system/_password -d "{\"password\":\"${KIBANA_PASSWORD}\"}" | grep -q "^{}"; do sleep 10; done

echo "All done!"