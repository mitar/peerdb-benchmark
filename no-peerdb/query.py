from pymongo import MongoClient
import config
import time

client = MongoClient(config.DATABASE_LOCATION)
db = client[config.DATABASE_NAME]

print "Checking collection counts"

persons = db['person']
tags = db['tag']
posts = db['post']
comments = db['comment']

print "Persons:", persons.count(), "Tags:", tags.count(),\
 "Posts:", posts.count(), "Comments:", comments.count()

start = time.time()
print "Querying all posts and content for each tag"

# iterate over all tags
for tag in tags.find({}, {'name': 1}):
	# we pretend that tag name is the only thing we have to begin with
	tag_name = tag['name']

	# get the tag
	tag = tags.find_one({'name': tag_name}, {'_id': 1})

	# query to get posts that include current tag
	tp = list(posts.find({'tags': tag['_id']}, {'body': 1, 'author': 1, 'tags': 1}))

	# query to get authors for all posts
	tp_authors = {person['_id']: person for person in persons.find({'_id': {'$in': [post['author'] for post in tp]}}, {'name': 1, 'picture': 1})}

	# query to get comment body for all comments of all posts
	tp_comments = {}
	for comment in comments.find({'post': {'$in': [post['_id'] for post in tp]}}, {'body': 1, 'post': 1}):
		if comment['post'] not in tp_comments:
			tp_comments[comment['post']] = []
		tp_comments[comment['post']].append(comment['body'])

	list_of_all_tags_ids = [tag for post in tp for tag in post['tags']]
	# query to get post tag names and descriptions for all posts
	tp_tags = {tag['_id']: tag for tag in tags.find({'_id': {'$in': list_of_all_tags_ids}}, {'name': 1, 'description': 1})}

	# making sure I got all info for each post
	# make a list of dicts where each dict contains post contents
	tp_contents = []
	for post in tp:
		tp_contents.append({
			"body": post['body'],
			"comments": tp_comments.get(post['_id'], []),
			"author_name": tp_authors[post['author']]['name'],
			"author_pic": tp_authors[post['author']]['picture'],
			"tags_name": [tp_tags[tag_id]['name'] for tag_id in post['tags']],
			"tags_description": [tp_tags[tag_id]['description'] for tag_id in post['tags']],
			})

print "Finished:", "elapsed time", time.time()-start
