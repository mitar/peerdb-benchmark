import os
import sys
import ddp
import json

METEOR_LOCATION = "ws://127.0.0.1:3000/websocket"

def main(args): 
	if len(args) < 3:
		print "Format: benchmark.py <path to jsons> <out fn for write times> <out fn for read times>"
		exit(-1)
	json_path = args[0]
	populate_out_fn = args[1]
	query_out_fn = args[2]

	json_fns = [json_path + fn for fn in os.listdir(json_path) if '.json' in fn]

	meteor = ddp.ConcurrentDDPClient(METEOR_LOCATION)

	meteor.start()

	for json_fn in sorted(json_fns):
		print "Current file is", json_fn.split('/')[-1]

		f = open(json_fn)
		settings = json.load(f)
		f.close()

		print "Populating"
		future = meteor.call('peerdb-populate-database', settings)

		result_message = future.get()
		if result_message.has_error():
			print "Meteor error: " + str(result_message.error)
			return

		(write_time, consistency_time) = result_message.result

		with open(populate_out_fn, "a") as populate_file:
			populate_file.write(json_fn + ' ' + str(write_time) + ' ' + str(consistency_time))

		print "Querying"
		future = meteor.call('peerdb-query-database')

		result_message = future.get()
		if result_message.has_error():
			print "Meteor error: " + str(result_message.error)
			return

		with open(query_out_fn, "a") as query_file:
			query_file.write(json_fn + ' ' + str(result_message.result))

	print "Disconnecting from Meteor (this might take quite some time, feel free to kill the program)"

	meteor.stop()
	meteor.join()


if __name__ == '__main__':
	main(sys.argv[1:])

