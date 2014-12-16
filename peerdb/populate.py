from pymongo import MongoClient, ASCENDING
import random
import config
import sys
import json
import string
import ddp
import time

def char_generator(size=6, chars=string.ascii_uppercase + string.digits):
	return ''.join(random.choice(chars) for _ in range(size))

# input: ordered objects, object_ids, fields to embed besides id, n
# output: peerdb compatible objects to embed
def random_objects(objects, object_ids, fields, n):
	assert len(objects) == len(object_ids)

	out = []
	for object_i in random.sample(xrange(len(objects)), n):
		obj = {'_id': object_ids[object_i]}
		for field in fields:
			obj[field] = objects[object_i][field]
		out.append(obj)

	return out

def random_id():
	return char_generator(17)

def main(args):
	if not args:
		sys.stderr.write("Supply parameter json file\n")
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

	sys.stderr.write("Dropping collections\n")

	db.Persons.drop()
	db.Tags.drop()
	db.Posts.drop()
	db.Comments.drop()

	sys.stderr.write("Waiting for database\n")

	future = meteor.call('wait-for-database')

	result_message = future.get()
	if result_message.has_error():
		sys.stderr.write("Meteor error: " + str(result_message.error)+ "\n")
		return

	future = meteor.call('reset-observe-callback-count')

	result_message = future.get()
	if result_message.has_error():
		sys.stderr.write("Meteor error: " + str(result_message.error)+ "\n")
		return

	sys.stderr.write("Adding collections\n")

	person_collection = db['Persons']
	tag_collection = db['Tags']
	post_collection = db['Posts']
	comment_collection = db['Comments']

	tag_collection.ensure_index([('name', ASCENDING)])
	post_collection.ensure_index([('tags.name', ASCENDING)])

	sys.stderr.write("Adding "+str(NUMBER_OF_PERSONS)+" persons\n")
	start = time.time()
	persons = []
	for person in range(NUMBER_OF_PERSONS):
		persons.append({
			"_id": random_id(),
			"name": char_generator(PERSON_NAME_SIZE),
			"bio": char_generator(PERSON_BIO_SIZE),
			"picture": char_generator(PERSON_PICTURE_SIZE)
			})
	person_ids = person_collection.insert(persons)

	sys.stderr.write("Adding "+str(NUMBER_OF_TAGS)+" tags\n")

	tags = []
	for i in range(NUMBER_OF_TAGS):
		tags.append({
			"_id": random_id(),
			"name": char_generator(TAG_NAME_SIZE),
			"description": char_generator(TAG_DESCRIPTION_SIZE)
			})
	tag_ids = tag_collection.insert(tags)

	sys.stderr.write("Adding "+str(NUMBER_OF_POSTS)+" posts\n")

	posts = []
	for i in range(NUMBER_OF_POSTS):
		posts.append({
			'_id': random_id(),
			'author': random_objects(persons, person_ids, ['name', 'picture'], 1)[0],
			'body': char_generator(POST_BODY_SIZE),
			'tags': random_objects(tags, tag_ids, ['name', 'description'], NUMBER_OF_TAGS_PER_POST)
			})
	post_ids = post_collection.insert(posts)

	sys.stderr.write("Adding "+str(NUMBER_OF_COMMENTS)+" comments\n")

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

	write_time = time.time()

	sys.stderr.write("Waiting for database\n")

	future = meteor.call('wait-for-database')
	result_message = future.get()
	if result_message.has_error():
		sys.stderr.write("Meteor error: " + str(result_message.error) + '\n')
		return
	else:
		callback_count = result_message.result
		sys.stderr.write(str(callback_count) + " PeerDB updates made\n")

	# there should be at least one update per post (in fact more like 3 * NUMBER_OF_COMMENTS)
	# TODO: Why not all updates are always made? Can we compute a strict number of them which had to be done and compare?
	assert callback_count > NUMBER_OF_POSTS

	end_time = time.time()

	# we subtract 60 seconds, an overhead made by wait-for-database
	print write_time - start, end_time - start - 60, callback_count

	sys.stderr.write("Disconnecting from Meteor (this might take quite some time, feel free to kill the program)\n")

	meteor.stop()
	meteor.join()

if __name__ == '__main__':
	main(sys.argv[1:])
