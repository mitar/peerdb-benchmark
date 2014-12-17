See branches for code for particular benchmarks.

## JSON generator ##

What does the JSON generator do?

Given a base JSON file, and an output directory, it varies size of embedded fields and numbers of documents and stores new JSON files into the output directory. Those JSON files can then be used with benchmark and query scripts as input to configure query parameters.

### Examples ###

* `mkdir json_out_path/`
* `python generate_jsons.py base_param.json json_out_path/ SIZE 10 100 1000`
  * Generates 3 output JSONs with `base_param.json`'s `PERSON_PICTURE`, `TAG_DESCRIPTION` and `COMMENT_BODY` set to each of the values `10`, `100`, `1000`
  * Saves each output JSON as: `json_out_path/size_10.json`, `json_out_path/size_100.json`, `json_out_path/size_1000.json`
* `python generate_jsons.py base_param.json json_out_path/ NUMBER 2 4 8 10`
    * Makes JSONs where all `NUMBER` values are multiplied by each value

## Docker scripts ##

All benchmarks together are available as a Docker image, with MongoDB and PostgreSQL installed in it: https://registry.hub.docker.com/u/mitar/peerdb-benchmark/

* `server1.sh` runs multiple Docker instances for all benchmarks with PeerDB having only one instance
* `server2.sh` runs only MongoDB Python PeerDB multiple Docker instances for multiple PeerDB instances: 2, 4, 6, 8, and 10
 * `server3.sh` runs only MongoDB Meteor PeerDB multiple Docker instances for multiple PeerDB instances: 2, 4, 6, 8, and 10

`collect.py` script connects to all Docker instances and reads `read.file` and `write.file` outputs.
