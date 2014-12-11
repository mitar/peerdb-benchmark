import subprocess as sbp
import os
import sys

ABSOLUTE_PATH = "/Users/apavel/code/mongo-python/peerdb-benchmark/peerdb/"

def main(args): 
	if len(args) < 3: 
		print "Format: benchmark.py <path to jsons> <out fn for write times> <out fn for read times>"
		exit(-1)
	json_path = args[0]
	populate_out_fn = args[1]
	query_out_fn = args[2]

	json_fns = [json_path + fn for fn in os.listdir(json_path) if '.json' in fn]

	for json_fn in json_fns:
		print "Current file is", json_fn.split('/')[-1]

		print "Populating"
		with open(os.devnull, 'w') as FNULL:
			t = sbp.check_output(['python', ABSOLUTE_PATH+'populate.py', json_fn], stderr=FNULL)

		with open(populate_out_fn, "a") as populate_file:
			populate_file.write(json_fn + ' ' + str(t))

		print "Querying"
		with open(os.devnull, 'w') as FNULL:
			t = sbp.check_output(['python', ABSOLUTE_PATH+'query.py'], stderr=FNULL)

		with open(query_out_fn, "a") as query_file:
			query_file.write(json_fn + ' ' + str(t))


if __name__ == '__main__':
	main(sys.argv[1:])

