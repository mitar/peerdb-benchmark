from pymongo import MongoClient, ASCENDING
import random
import config
import sys
import json
import string
import time

def char_generator(size=6, chars=string.ascii_uppercase + string.digits):
	return ''.join(random.choice(chars) for _ in range(size))

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

	sys.stderr.write("Dropping collections\n")

	db.person.drop()
	db.tag.drop()
	db.post.drop()
	db.comment.drop()

	sys.stderr.write("Adding collections\n")

	person_collection = db['person']
	tag_collection = db['tag']
	post_collection = db['post']
	comment_collection = db['comment']

	tag_collection.ensure_index([('name', ASCENDING)])

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
			'author': random.choice(person_ids),
			'body': char_generator(POST_BODY_SIZE),
			'tags': random.sample(tag_ids, NUMBER_OF_TAGS_PER_POST)
			})
	post_ids = post_collection.insert(posts)

	sys.stderr.write("Adding "+str(NUMBER_OF_COMMENTS)+" comments\n")

	comments = []
	for i in range(NUMBER_OF_COMMENTS): 
		comments.append({
			"_id": random_id(),
			"body": char_generator(COMMENT_BODY_SIZE),
			# TODO: We should use here some long-tail distribution (20% of posts has 80% of comments)
			"post": random.choice(post_ids)
			})
	comment_ids = comment_collection.insert(comments)

	print time.time()-start

	sys.stderr.write("Done\n")

if __name__ == '__main__':
	main(sys.argv[1:])
