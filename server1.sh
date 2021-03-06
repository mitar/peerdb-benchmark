#!/bin/bash -e

docker pull mitar/peerdb-benchmark

docker run -d --name postgresql-python-only mitar/peerdb-benchmark
sleep 30
docker exec -d postgresql-python-only bash -c \
  "cd /benchmark/peerdb-benchmark-postgresql-python/python_only/; \
  python /benchmark/peerdb-benchmark-postgresql-python/python_only/benchmark.py /benchmark/jsons/ /benchmark/write.file /benchmark/read.file >>/benchmark/log 2>&1;"

docker run -d --name postgresql-python-django mitar/peerdb-benchmark
sleep 30
docker exec -d postgresql-python-django bash -c \
  "cd /benchmark/peerdb-benchmark-postgresql-python/django_project/; \
  python /benchmark/peerdb-benchmark-postgresql-python/django_project/benchmark.py /benchmark/jsons/ /benchmark/write.file /benchmark/read.file >>/benchmark/log 2>&1;"

docker run -d --name mongodb-python-nopeerdb mitar/peerdb-benchmark
sleep 30
docker exec -d mongodb-python-nopeerdb bash -c \
  "cd /benchmark/peerdb-benchmark-mongodb-python/no-peerdb/;
  python /benchmark/peerdb-benchmark-mongodb-python/no-peerdb/benchmark.py /benchmark/jsons/ /benchmark/write.file /benchmark/read.file >>/benchmark/log 2>&1;"

docker run -d --name mongodb-python-peerdb-1 mitar/peerdb-benchmark
sleep 30
docker exec -d mongodb-python-peerdb-1 bash -c \
  "cd /benchmark/peerdb-benchmark-mongodb-meteor/; \
  ./run-peerdb.sh 1 >>/benchmark/log 2>&1; \
  sleep 10; \
  cd /benchmark/peerdb-benchmark-mongodb-python/peerdb/; \
  python /benchmark/peerdb-benchmark-mongodb-python/peerdb/benchmark.py /benchmark/jsons/ /benchmark/write.file /benchmark/read.file >>/benchmark/log 2>&1;"

docker run -d --name mongodb-meteor-collection mitar/peerdb-benchmark
sleep 30
docker exec -d mongodb-meteor-collection bash -c \
  "cd /benchmark/peerdb-benchmark-mongodb-meteor/; \
  ./run-peerdb.sh 1 >>/benchmark/log 2>&1; \
  sleep 10; \
  python /benchmark/peerdb-benchmark-mongodb-meteor/benchmark-collection.py /benchmark/jsons/ /benchmark/write.file /benchmark/read.file >>/benchmark/log 2>&1;"

docker run -d --name mongodb-meteor-peerdb-1 mitar/peerdb-benchmark
sleep 30
docker exec -d mongodb-meteor-peerdb-1 bash -c \
  "cd /benchmark/peerdb-benchmark-mongodb-meteor/; \
  ./run-peerdb.sh 1 >>/benchmark/log 2>&1; \
  sleep 10; \
  python /benchmark/peerdb-benchmark-mongodb-meteor/benchmark-peerdb.py /benchmark/jsons/ /benchmark/write.file /benchmark/read.file >>/benchmark/log 2>&1;"
