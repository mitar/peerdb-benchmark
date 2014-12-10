from pymongo import MongoClient
import random
import config
import sys
import json
import string

def char_generator(size=6, chars=string.ascii_uppercase + string.digits):
	return ''.join(random.choice(chars) for _ in range(size))

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

	PERSON_NAME = char_generator(param['SIZE']['PERSON_NAME'])
	PERSON_BIO = char_generator(param['SIZE']['PERSON_BIO'])
	PERSON_PICTURE = char_generator(param['SIZE']['PERSON_PICTURE'])
	TAG_NAME = char_generator(param['SIZE']['TAG_NAME'])
	TAG_DESCRIPTION = char_generator(param['SIZE']['TAG_DESCRIPTION'])
	POST_BODY = char_generator(param['SIZE']['POST_BODY'])
	COMMENT_BODY = char_generator(param['SIZE']['COMMENT_BODY'])

	client = MongoClient(config.DATABASE_LOCATION) 
	db = client[config.DATABASE_NAME]

	print "Dropping collections"

	db.person.drop()
	db.tag.drop()
	db.post.drop()
	db.comment.drop()

	print "Adding collections"

	person_collection = db['person']
	tag_collection = db['tag']
	post_collection = db['post']
	comment_collection = db['comment']

	print "Adding", NUMBER_OF_PERSONS, "persons"

	persons = []
	for person in range(NUMBER_OF_PERSONS): 
		# TODO: Add picture
		persons.append({
			"name": PERSON_NAME, 
			"bio": PERSON_BIO,
			"picture": PERSON_PICTURE
			})
	person_ids = person_collection.insert(persons)

	print "Adding", NUMBER_OF_TAGS, "tags"

	tags = []
	for i in range(NUMBER_OF_TAGS): 
		tags.append({
			"name": TAG_NAME,
			"description": TAG_DESCRIPTION
			})
	tag_ids = tag_collection.insert(tags)


	print "Adding", NUMBER_OF_POSTS,"posts"

	posts = []
	for i in range(NUMBER_OF_POSTS): 
		posts.append({
			'author': random.choice(person_ids),
			'body': POST_BODY,
			'tags': random.sample(tag_ids, NUMBER_OF_TAGS_PER_POST)
			})
	post_ids = post_collection.insert(posts)

	print "Adding", NUMBER_OF_COMMENTS, "comments"

	comments = []
	for i in range(NUMBER_OF_COMMENTS): 
		comments.append({
			"body": COMMENT_BODY,
			"post": random.choice(post_ids)
			})
	comment_ids = comment_collection.insert(comments)

if __name__ == '__main__':
	main(sys.argv[1:])

