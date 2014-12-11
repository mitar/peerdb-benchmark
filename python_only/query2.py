import psycopg2
import config
import time
import sys

conn = psycopg2.connect(config.DATABASE_INFO)
tags_cur = conn.cursor()
cur = conn.cursor()

sys.stderr.write("Checking collection counts\n")

cur.execute("""SELECT COUNT(*) from person""")
persons_count = cur.fetchone()[0]
cur.execute("""SELECT COUNT(*) from tag""")
tags_count = cur.fetchone()[0]
cur.execute("""SELECT COUNT(*) from post""")
posts_count = cur.fetchone()[0]
cur.execute("""SELECT COUNT(*) from comment""")
comments_count = cur.fetchone()[0]

sys.stderr.write(' '.join(["Persons:", str(persons_count), "Tags:", str(tags_count),
"Posts:", str(posts_count), "Comments:", str(comments_count)]) + '\n')

sys.stderr.write("Querying all posts and content for each tag\n")

# this is a version of a query where we do not transmit any data
# multiple times, but we instead rather do multiple queries

start = time.time()
# iterate over all tags
tags_cur.execute("""SELECT name from tag""")
# we pretend that tag name is the only thing we have to begin with
for (cur_tag_name,) in tags_cur:
	# query to get posts that include current tag
	cur.execute("""
		SELECT post.post_id, post.body, person.name, person.picture
		FROM post
		INNER JOIN person ON (post.author = person.person_id)
		INNER JOIN post_tag ON (post.post_id = post_tag.post_id)
		INNER JOIN tag ON (post_tag.tag_id = tag.tag_id)
		WHERE tag.name = %(cur_tag_name)s
	""", {'cur_tag_name': cur_tag_name})
	tp = cur.fetchall()

	post_ids = [post[0] for post in tp]

	# query to get comment body for all comments of all posts
	tp_comments = {}
	cur.execute("""
		SELECT body, post
		FROM comment
		WHERE post = ANY(%(post_ids)s)
	""", {'post_ids': post_ids})
	for (comment_body, comment_post) in cur:
		if comment_post not in tp_comments:
			tp_comments[comment_post] = []
		tp_comments[comment_post].append(comment_body)

	# query to get all tag ids for all posts
	post_tags = {}
	list_of_all_tags_ids = []
	cur.execute("""
		SELECT post_tag.post_id, tag.tag_id
		FROM post_tag
		INNER JOIN tag ON (post_tag.tag_id = tag.tag_id)
		WHERE post_tag.post_id = ANY(%(post_ids)s)
	""", {'post_ids': post_ids})
	for (post_id, tag_id) in cur:
		if post_id not in post_tags:
			post_tags[post_id] = []
		post_tags[post_id].append(tag_id)
		list_of_all_tags_ids.append(tag_id)

	# query to get names and descriptions for all tags
	tags = {}
	cur.execute("""
		SELECT tag_id, name, description
		FROM tag
		WHERE tag_id = ANY(%(list_of_all_tags_ids)s)
	""", {'list_of_all_tags_ids': list_of_all_tags_ids})
	for (tag_id, tag_name, tag_description) in cur:
		tags[tag_id] = (tag_name, tag_description)

	# making sure I got all info for each post
	# make a list of dicts where each dict contains post contents
	tp_contents = []
	for post in tp:
		tp_contents.append({
			"body": post[1],
			"comments": tp_comments.get(post[0], []),
			"author_name": post[2],
			"author_pic": post[3],
			"tags_name": [tags[tag_id][0] for tag_id in post_tags[post[0]]],
			"tags_description": [tags[tag_id][1] for tag_id in post_tags[post[0]]],
			})

print time.time()-start

tags_cur.close()
cur.close()
conn.close()
