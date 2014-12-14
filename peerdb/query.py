from pymongo import MongoClient
import config
import time
import sys

client = MongoClient(config.DATABASE_LOCATION) 
db = client[config.DATABASE_NAME]

sys.stderr.write("Checking collection counts\n")

persons = db['Persons']
tags = db['Tags']
posts = db['Posts']
comments = db['Comments']

sys.stderr.write(' '.join(["Persons:", str(persons.count()), "Tags:", str(tags.count()),
"Posts:", str(posts.count()), "Comments:", str(comments.count())]) + '\n')

sys.stderr.write("Querying all posts and content for each tag\n")

start = time.time()
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
			# TODO: Why it sometimes does not sync the comments?
			"comments": [comment.get('body', '') for comment in post.get('comments', [])],
			"author_name": post['author']['name'],
			"author_picture": post['author']['picture'],
			"tags_name": [tag['name'] for tag in post['tags']],
			"tags_description": [tag['description'] for tag in post['tags']],
			})

print time.time()-start
