This branch consists of Python programs:
 * to populate MongoDB database
   * with PeerDB help (`peerdb/populate.py`)
   * without PeerDB help (`no-peerdb/populate.py`)
 * to read from MongoDB database
   * using recursive MongoDB queries
     * (TBD) reading related documents iteratively, storing minimal set of documents in memory
     * reading related documents in bulk, storing all documents in memory and reconstructing them (`no-peerdb/query.py`)
   * using embedded documents made by PeerDB (`peerdb/query.py`)

How to make it work: 
* Modify `config.py` in `no-peerdb/` to MongoDB database without PeerDB running
  * change `DATABASE_NAME`
  * change `DATABASE_LOCATION`
* Modify `config.py` in `peerdb/` to MongoDB database with PeerDB running 
  * change `DATABASE_NAME`
  * change `DATABASE_LOCATION`
* To populate database: 
  * No PeerDB: `python no-peerdb/populate.py <path to parameter json>`
  * With PeerDB: `python peerdb/populate.py <path to parameter json>`
  * sample parameter json and programs to generate more of them are available in `master` branch
* To query database
  * No PeerDB: `python no-peerdb/query.py`
  * With PeerDB: `python peerdb/query.py`

The queries aggregate content of all posts for each tag name but do not output this data.

`benchmark.py` scripts conveniently run both populate and query for all JSON files in a directory.
