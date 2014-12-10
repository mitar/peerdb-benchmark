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
for tag in tags.find():
	# query to get posts that include current tag
	# making sure I got all info for each post
	# make a list of dicts where each dict contains post contents
	tp_contents = []
	for post in posts.find({'tags.name': tag['name']}):
		tp_contents.append({
			"body": post['body'],
			"comments": [comment['body'] for comment in post['comments']],
			"author_name": post['author']['name'],
			"author_pic": post['author']['picture'],
			"tags": [tag['name'] for tag in post['tags']],
			})

print "Finished:", "elapsed time", time.time()-start
