# use generate_jsons.py <base_json_fn> <out_path> <type> <values>

import json
import sys

def main(args): 
	
	if len(args) < 4: 
		sys.stderr.write("Format is generate_jsons.py <base_json_fn> <out_path> <type> <value 1> <value 2> ...\n")
		exit(-1)

	in_file = open(args[0])
	in_json = json.load(in_file)
	in_file.close()

	out_path = args[1]
	var_type = args[2]
	values = [int(v) for v in args[3:]]

	if var_type.lower() == "size":
		var_to_change = ["PERSON_PICTURE", "TAG_DESCRIPTION", "COMMENT_BODY"]

		# iterate through each value
		for value in values: 

			for var in var_to_change: 
				# set each variable to the given value
				in_json["SIZE"][var] = value

			# save json for each value with all relevant variables changed
			out_file = open(out_path + str(var_type.lower()) + '_' + str(value) + '.json', 'w')
			json.dump(in_json, out_file)
			out_file.close()

	elif var_type.lower() == "number": 
		var_to_change = ["POSTS", "TAGS", "PERSONS", "COMMENTS", "TAGS_PER_POST"]

		for value in values: 
			
			for var in var_to_change: 
				# multiply each variable by the given value
				in_json['NUMBER'][var] = in_json['NUMBER'][var]*value

			# save json for each value with all relevant variables changed
			out_file = open(out_path + str(var_typ.lower()) + '_' + str(value) + '.json', 'w')
			json.dump(in_json, out_file)
			out_file.close()

if __name__ == '__main__':
	main(sys.argv[1:])