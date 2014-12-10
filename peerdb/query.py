from pymongo import MongoClient
import config
import time

client = MongoClient(config.DATABASE_LOCATION) 
db = client[config.DATABASE_NAME]

print "Checking collection counts"

persons = db['Persons']
tags = db['Tags']
posts = db['Posts']
comments = db['Comments']

print "Person:", persons.count(), "Tag:", tags.count(),\
 "Post:", posts.count(), "Comment:", comments.count()

start = time.time()
print "Querying all posts and content for each tag"

# iterate over all tags
for tag in tags.find({}, {'name': 1}):
	# we pretend that tag name is the only thing we have to begin with
	tag_name = tag['name']

	# query to get posts that include current tag
	# making sure I got all info for each post
	# make a list of dicts where each dict contains post contents
	tp_contents = []
	for post in posts.find({'tags.name': tag_name}, {'body': 1, 'comments.body': 1, 'author.name': 1, 'author.picture': 1, 'tags.name': 1, 'tags.description' : 1}):
		tp_contents.append({
			"body": post['body'],
			"comments": [comment['body'] for comment in post['comments']],
			"author_name": post['author']['name'],
			"author_picture": post['author']['picture'],
			"tags_name": [tag['name'] for tag in post['tags']],
			"tags_description": [tag['description'] for tag in post['tags']],
			})

print "Finished:", "elapsed time", time.time()-start
