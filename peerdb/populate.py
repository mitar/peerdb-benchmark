from pymongo import MongoClient
import random
import config
import sys
import json
import string
import ddp

def char_generator(size=6, chars=string.ascii_uppercase + string.digits):
	return ''.join(random.choice(chars) for _ in range(size))

# input: ordered objects, object_ids, fields to embed besides id, n
# output: peerdb compatible objects to embed
def random_objects(objects, object_ids, fields, n):
	assert len(objects) == len(object_ids)
	len_objects = len(objects)

	out = []
	for i in range(n):
		object_i = random.randrange(len_objects)
		obj = {'_id': object_ids[object_i]}
		for field in fields:
			obj[field] = objects[object_i][field]
		out.append(obj)

	return out

def random_id():
	return char_generator(17)

def main(args): 
	if not args: 
		print "Supply parameter json file: python populate.py sample_parameters.json"
		exit(-1)

	f = open(args[0])
	param = json.load(f)
	f.close()

	NUMBER_OF_PERSONS = param['NUMBER']['PERSONS']
	NUMBER_OF_TAGS = param['NUMBER']['TAGS']
	NUMBER_OF_POSTS = param['NUMBER']['POSTS']
	NUMBER_OF_TAGS_PER_POST = param['NUMBER']['TAGS_PER_POST']
	NUMBER_OF_COMMENTS = param['NUMBER']['COMMENTS']

	PERSON_NAME_SIZE = param['SIZE']['PERSON_NAME']
	PERSON_BIO_SIZE = param['SIZE']['PERSON_BIO']
	PERSON_PICTURE_SIZE = param['SIZE']['PERSON_PICTURE']
	TAG_NAME_SIZE = param['SIZE']['TAG_NAME']
	TAG_DESCRIPTION_SIZE = param['SIZE']['TAG_DESCRIPTION']
	POST_BODY_SIZE = param['SIZE']['POST_BODY']
	COMMENT_BODY_SIZE = param['SIZE']['COMMENT_BODY']

	client = MongoClient(config.DATABASE_LOCATION)
	db = client[config.DATABASE_NAME]

	meteor = ddp.ConcurrentDDPClient(config.METEOR_LOCATION)

	meteor.start()

	print "Dropping collections"

	db.Persons.drop()
	db.Tags.drop()
	db.Posts.drop()
	db.Comments.drop()

	print "Waiting for database"

	future = meteor.call('wait-for-database')

	result_message = future.get()
	if result_message.has_error():
		print "Meteor error:", result_message.error
		return

	future = meteor.call('reset-observe-callback-count')

	result_message = future.get()
	if result_message.has_error():
		print "Meteor error:", result_message.error
		return

	print "Adding collections"

	person_collection = db['Persons']
	tag_collection = db['Tags']
	post_collection = db['Posts']
	comment_collection = db['Comments']

	print "Adding", NUMBER_OF_PERSONS, "persons"

	persons = []
	for person in range(NUMBER_OF_PERSONS):
		persons.append({
			"_id": random_id(),
			"name": char_generator(PERSON_NAME_SIZE),
			"bio": char_generator(PERSON_BIO_SIZE),
			"picture": char_generator(PERSON_PICTURE_SIZE)
			})
	person_ids = person_collection.insert(persons)

	print "Adding", NUMBER_OF_TAGS, "tags"

	tags = []
	for i in range(NUMBER_OF_TAGS): 
		tags.append({
			"_id": random_id(),
			"name": char_generator(TAG_NAME_SIZE),
			"description": char_generator(TAG_DESCRIPTION_SIZE)
			})
	tag_ids = tag_collection.insert(tags)

	print "Adding", NUMBER_OF_POSTS, "posts"

	posts = []
	for i in range(NUMBER_OF_POSTS): 
		posts.append({
			'_id': random_id(),
			'author': random_objects(persons, person_ids, ['name', 'picture'], 1)[0],
			'body': char_generator(POST_BODY_SIZE),
			'tags': random_objects(tags, tag_ids, ['name', 'description'], NUMBER_OF_TAGS_PER_POST)
			})
	post_ids = post_collection.insert(posts)

	print "Adding", NUMBER_OF_COMMENTS, "comments"

	comments = []
	for i in range(NUMBER_OF_COMMENTS): 
		comments.append({
			"_id": random_id(),
			"body": char_generator(COMMENT_BODY_SIZE),
			"post": {
				# TODO: We should use here some long-tail distribution (20% of posts has 80% of comments)
				'_id': random.choice(post_ids),
				}
			})
	comment_ids = comment_collection.insert(comments)

	print "Waiting for database"

	future = meteor.call('wait-for-database')
	result_message = future.get()
	if result_message.has_error():
		print "Meteor error:", result_message.error
		return
	else:
		print result_message.result, "PeerDB updates made"

	print "Confirming things inserted:", \
		len(person_ids), len(tag_ids), len(post_ids), len(comment_ids)

	print "Disconnecting from Meteor (this might take quite some time, feel free to kill the program)"

	meteor.stop()
	meteor.join()

if __name__ == '__main__':
	main(sys.argv[1:])
