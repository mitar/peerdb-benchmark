#!/bin/bash -e

docker pull mitar/peerdb-benchmark

for I in 2 4 6 8 10; do
  docker run -d --name "mongodb-python-peerdb-$I" mitar/peerdb-benchmark
  sleep 30
  docker exec -d "mongodb-python-peerdb-$I" bash -c \
    "cd /benchmark/peerdb-benchmark-mongodb-meteor/; \
    ./run-peerdb.sh $I >>/benchmark/log 2>&1; \
    sleep 10; \
    cd /benchmark/peerdb-benchmark-mongodb-python/peerdb/; \
    python /benchmark/peerdb-benchmark-mongodb-python/peerdb/benchmark.py /benchmark/jsons/ /benchmark/write.file /benchmark/read.file >>/benchmark/log 2>&1;"
done
