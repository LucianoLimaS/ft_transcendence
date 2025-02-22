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
  echo "Creating certificates"
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

# Wait for Elasticsearch to be ready
echo "Waiting for Elasticsearch availability"
until curl -s -X GET --cacert /usr/share/elasticsearch/config/certs/ca/ca.crt \
  -u "elastic:${ELASTIC_PASSWORD}" "https://elasticsearch:9200/_cluster/health" | grep -q '"status":"green"'; do
  echo "Elasticsearch still initializing..."
  sleep 10
done

echo "Setting kibana_system password"
until curl -s -X POST --cacert /usr/share/elasticsearch/config/certs/ca/ca.crt -u "elastic:${ELASTIC_PASSWORD}" -H "Content-Type: application/json" https://elasticsearch:9200/_security/user/kibana_system/_password -d "{\"password\":\"${KIBANA_PASSWORD}\"}" | grep -q "^{}"; do 
  echo "Waiting for Elasticsearch to allow password change..."
  sleep 10
done

# Wait for Kibana to be ready
echo "Waiting for Kibana availability"
until curl -s -X GET --cacert /usr/share/elasticsearch/config/certs/ca/ca.crt \
  -u "elastic:${ELASTIC_PASSWORD}" "http://kibana:5601/api/status" | grep -q '"overall":{"level":"available"'; do
  echo "Kibana still initializing..."
  sleep 10
done

# Import dashboards
max_retries=5
attempt=0
success=false

while [ $attempt -lt $max_retries ]; do
  echo "Attempt $(($attempt + 1)) to import the dashboard..."
  response=$(curl -v -s -X POST "http://kibana:5601/api/saved_objects/_import" \
    -u "elastic:${ELASTIC_PASSWORD}" \
    --cacert /usr/share/elasticsearch/config/certs/ca/ca.crt \
    -H "kbn-xsrf: true" \
    -H "Content-Type: multipart/form-data" \
    -F "file=@/usr/share/kibana/kibana_export.ndjson")

  if echo "$response" | grep -q "success"; then
    echo "Dashboard imported successfully!"
    success=true
    break
  else
    echo "Failed to import dashboard: $response"
    sleep 30
  fi
  attempt=$((attempt + 1))
done

if [ "$success" = false ]; then
  echo "Failed to import dashboard after $max_retries attempts."
fi

echo "All done!"