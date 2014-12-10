This branch consists of Python programs:
 * to populate MongoDB database
   * with PeerDB help
   * without PeerDB help
 * to read from MongoDB database
   * using recursive MongoDB queries
     * reading related documents iteratively
     * TODO: reading related documents in bulk
   * using embedded documents made by PeerDB

How to make it work: 
* Modify config.py in no-peerdb/ to mongodb without peerdb
  * change DATABASE_NAME
  * change DATABASE_LOCATION
* Modify config.py in peerdb/ to mongodb with peerdb 
  * change DATABASE_NAME
  * change DATABASE_LOCATION
* To populate database: 
  * No peerdb: python no-peerdb/populate.py
  * With peerdb: python peerdb/populate.py
* To query database (only iterative reading for now)
  * No peerdb: python no-peerdb/query.py
  * With peerdb: python peerdb/query.py
* The query.py's aggregate content of all posts for each tag but do not output this data