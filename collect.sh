#!/bin/bash -e

for container in $(docker ps | grep "mitar/peerdb-benchmark" | awk '{print $1}'); do
  echo "read" $(docker inspect --format '{{ .Name }}' "$container")
  docker exec "$container" cat /benchmark/read.file
  echo "write" $(docker inspect --format '{{ .Name }}' "$container")
  docker exec "$container" cat /benchmark/write.file
done
