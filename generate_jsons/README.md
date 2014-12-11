What does the json generator do?
* Given a base json, and an outfile it varies size and numbers
* Samples: 
  * mkdir json_out_path/
  * python generate_jsons.py base_param.json json_out_path/ SIZE 10 100 1000
    * Generates 3 output jsons with base_param.json's "PERSON_PICTURE", "TAG_DESCRIPTION" and "COMMENT_BODY" set to each of the values 10 100 1000
    * Saves each output json as: json_out_path/size_10.json, json_out_path/size_100.json, json_out_path/size_1000.json
  * python generate_jsons.py base_param.json json_out_path/ NUMBER 2 4 8 10
    * Makes jsons where all NUMBER values are multiplied by each value
