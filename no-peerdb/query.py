from pymongo import MongoClient
import random
import config
import time

client = MongoClient() 
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
for tag in tags.find():

	# query to get posts that include current tag (TODO: better way to do this?)
	tp = [post for post in posts.find() if tag['_id'] in post['tags']]

	# query to get author for each post
	tp_authors = [persons.find_one({'_id': post['author']}) \
		for post in tp]

	# query to get comment body for each comment on a post
	# .find returns cusor, so iterate through this to get each comment
	tp_comments = [[c for c in comments.find({'post': post['_id']})]
		for post in tp]

	# query to get post tag names for each post
	tp_tags = [[tags.find_one({'_id': did}) for did in post['tags']] for post in tp]

	# making sure I got all info for each post
	# make a list of dicts where each dict contains post contents
	tp_contents = []
	for i in range(len(tp)):
		post = tp[i] 
		tp_contents.append({
			"body": post['body'],
			"comments": [c['body'] for c in tp_comments[i]],
			"author_name": tp_authors[i]['name'],
			"author_pic": tp_authors[i]['picture'],
			"tags": [t['name'] for t in tp_tags[i]]
			})
print "Finished:", "elapsed time", time.time()-start

