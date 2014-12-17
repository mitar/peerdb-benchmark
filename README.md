This branch consists of a Meteor app which exposes two sets of Meteor methods:
 * to populate MongoDB database
   * with PeerDB help (`peerdb-populate-database`)
   * without PeerDB help (`collections-populate-database`)
 * to read from MongoDB database
   * to read one query
     * using recursive MongoDB queries
       * (TBD) reading related documents iteratively, storing minimal set of documents in memory
       * reading related documents in bulk, storing all documents in memory and reconstructing them (`collections-query-database`)
     * using embedded documents made by PeerDB (`peerdb-query-database`)
   * (TBD) to read a streaming query
     * using recursive MongoDB queries
       * reading related documents iteratively
       * reading related documents in bulk
     * using embedded documents made by PeerDB

Just running a Meteor application allows one to use it as a helper instance for use when querying the database from another programming language. We use this in `mongodb-python` branch for a Python program which uses PeerDB.

`run-peerdb.sh` script provides an easy way to start a Meteor app with multiple instances:

```
run-peerdb.sh 2
```

This will run Meteor app 2 instances, on different ports. It expects that Meteor app was bundled into the `bundle` directory with:

```
meteor build . --directory
```

`benchmark-collection.py` script connects to the Meteor app and runs `collections-populate-database` and `collections-query-database` methods. ` benchmark-peerdb.py` script runs `peerdb-populate-database` and `peerdb-query-database` methods.
