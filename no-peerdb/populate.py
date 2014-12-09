from pymongo import MongoClient
import random

DATABASE_NAME = 'nopeerdb'

# same as https://github.com/mitar/peerdb-benchmark/
# blob/mongodb-meteor/server/populate.coffee
NUMBER_OF_PERSONS = 100
NUMBER_OF_TAGS = 100
NUMBER_OF_POSTS = 1000
NUMBER_OF_TAGS_PER_POST = 10
NUMBER_OF_COMMENTS = 10000

client = MongoClient() # default localhost:27017
db = client[DATABASE_NAME]

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
		"name": "name", 
		"bio": "bio",
		"picture": "picture"
		})
person_ids = person_collection.insert(persons)

print "Adding", NUMBER_OF_TAGS, "tags"

tags = []
for i in range(NUMBER_OF_TAGS): 
	tags.append({
		"name": "name",
		"description": "description"
		})
tag_ids = tag_collection.insert(tags)


print "Adding", NUMBER_OF_POSTS,"posts"

posts = []
for i in range(NUMBER_OF_POSTS): 
	posts.append({
		'author': random.choice(person_ids),
		'body': 'body',
		'tags': random.sample(tag_ids, NUMBER_OF_TAGS_PER_POST)
		})
post_ids = post_collection.insert(posts)

print "Adding", NUMBER_OF_COMMENTS, "comments"

comments = []
for i in range(NUMBER_OF_COMMENTS): 
	comments.append({
		"body": "body",
		"post": random.choice(post_ids)
		})
comment_ids = comment_collection.insert(comments)

