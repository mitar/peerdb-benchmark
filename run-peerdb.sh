#!/bin/bash -e

# In "bundle" subdirectory app should be build to:
# meteor build . --directory
cd bundle

NODE=$(find /root/.meteor/ -path '*bin/node' | sort | tail -n 1)

export NODE_PATH="$(dirname $(dirname "$NODE"))/lib/node_modules"
export NODE_ENV="production"
export MONGO_URL="mongodb://127.0.0.1:27017/meteor"
export MONGO_OPLOG_URL="mongodb://127.0.0.1:27017/local"

if [[ -z "$1" ]]; then
	export PEERDB_INSTANCES="1"
else
  export PEERDB_INSTANCES="$1"
fi

for I in $(seq 1 $PEERDB_INSTANCES); do
  PEERDB_INSTANCE="$((I-1))" PORT="$((2900 + 100 * I))" ROOT_URL="http://127.0.0.1:$((2900 + 100 * I))" "$NODE" --max-old-space-size=8192 main.js &
done
