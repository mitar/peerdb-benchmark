#!/bin/bash -e

docker pull mitar/peerdb-benchmark

for I in 2 4 6 8 10; do
  docker run -d --name "mongodb-meteor-peerdb-$I" mitar/peerdb-benchmark
  sleep 20
  docker exec -d "mongodb-meteor-peerdb-$I" bash -c \
    "cd /benchmark/peerdb-benchmark-mongodb-meteor/; \
    ./run-peerdb.sh $I \
    python /benchmark/peerdb-benchmark-mongodb-meteor/benchmark-peerdb.py /benchmark/jsons/ /benchmark/write.file /benchmark/read.file >/benchmark/log 2>&1"
done
