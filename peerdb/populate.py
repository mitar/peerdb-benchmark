from pymongo import MongoClient
import random
import config

# input: ordered objects, object_ids, fields to embed besides id, n
# output: peerdb compatible objects to embed
def random_objects(objects, object_ids, fields, n): 
	object_ids = random.sample(object_ids, n)
	out = []
	for i in range(len(object_ids)):
		obj = {'_id': object_ids[i]}
		for field in fields: 
			obj[field] = objects[i][field]
		out.append(obj)
	return out

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

print "Adding", config.NUMBER_OF_PERSONS, "persons"

persons = []
for person in range(config.NUMBER_OF_PERSONS): 
	# TODO: Add picture
	persons.append({
		"name": "name", 
		"bio": "bio",
		"picture": "picture"
		})
person_ids = person_collection.insert(persons)

print "Adding", config.NUMBER_OF_TAGS, "tags"

tags = []
for i in range(config.NUMBER_OF_TAGS): 
	tags.append({
		"name": "name",
		"description": "description"
		})
tag_ids = tag_collection.insert(tags)


print "Adding", config.NUMBER_OF_POSTS,"posts"

posts = []
for i in range(config.NUMBER_OF_POSTS): 
	posts.append({
		'author': random_objects(persons, person_ids, ['name', 'picture'], 1)[0],
		'body': 'body',
		'tags': random_objects(tags, tag_ids, ['name'], config.NUMBER_OF_TAGS_PER_POST)
		})
post_ids = post_collection.insert(posts)
print posts[0]

print "Adding", config.NUMBER_OF_COMMENTS, "comments"

comments = []
for i in range(config.NUMBER_OF_COMMENTS): 
	comments.append({
		"body": "body",
		"post": random.choice(post_ids)
		})
comment_ids = comment_collection.insert(comments)

print "Confirming things inserted:", \
	len(person_ids), len(tag_ids), len(post_ids), len(comment_ids)