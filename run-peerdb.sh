#!/bin/bash -e

# In "build" subdirectory app should be build to:
# meteor build ./build --directory
cd build

NODE=$(find /root/.meteor/ -path '*bin/node')

export NODE_ENV="PRODUCTION"
export MONGO_URL="mongodb://localhost:27017/meteor"
export MONGO_OPLOG_URL="mongodb://localhost:27017/local"

if [[ -z "$1" ]]; then
	export PEERDB_INSTANCES="1"
else
  export PEERDB_INSTANCES="$1"
fi

for I in $(seq 1 $PEERDB_INSTANCES); do
  PEERDB_INSTANCE="$((I-1))" PORT="$((2900 + 100 * I))" "$NODE" main.js &
done
