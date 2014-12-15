#!/bin/bash -e

for I in 2 4 6 8 10; do
  docker run -d --name "mongodb-python-peerdb-$I" peerdb-benchmark
  sleep 20
  docker exec -d "mongodb-python-peerdb-$I" bash -c \
    "cd /benchmark/peerdb-benchmark-mongodb-meteor/; \
    ./run-peerdb.sh $I \
    cd /benchmark/peerdb-benchmark-mongodb-python/peerdb/; \
    python /benchmark/peerdb-benchmark-mongodb-python/peerdb/benchmark.py /benchmark/jsons/ /benchmark/write.file /benchmark/read.file >/benchmark/log 2>&1"
done
