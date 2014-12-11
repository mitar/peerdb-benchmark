import psycopg2
import random
import config
import time
import sys

conn=psycopg2.connect(config.DATABASE_INFO)
cur = conn.cursor()

# get all tags
cur.execute("""SELECT tag_id from tag""")
tag_ids = cur.fetchall()

# put tag ids into random order
tag_ids = random.sample(tag_ids, len(tag_ids))

start = time.time()
sys.stderr.write("Querying\n")
for tag_id in tag_ids: 

	# join for tag queries
	cur.execute("""SELECT post.* FROM post 
		INNER JOIN post_tag 
		ON (post.post_id = post_tag.post_id) 
		WHERE post_tag.tag_id = """ + str(tag_id[0]) + ';')
	posts = cur.fetchall()

	comments = []
	tags = []
	authors = []

	# for each post, make queries for comments, author, and tags
	for post in posts: 
		#import pdb; pdb.set_trace()
		post_id = post[0]

		cur.execute("""SELECT comment.body
			FROM comment 
			WHERE post = """ + str(post_id) + ';')
		post_comments = cur.fetchall()
		comments.append(post_comments)

		cur.execute("""SELECT person.name, person.picture
			FROM person 
			WHERE person.person_id = """ + str(post[2]) + ';')
		post_author = cur.fetchall()
		authors.append(post_author[0])

		cur.execute("""SELECT tag.name
			FROM tag 
			INNER JOIN post_tag
			ON (tag.tag_id = post_tag.tag_id) 
			WHERE post_tag.post_id = """ + str(post_id) + ';')
		post_tags = cur.fetchall()
		tags.append(post_tags)

	# showing we have all the info
	out = []
	for i in range(len(posts)): 
		out.append({
			'body': posts[i][1],
			'comments': [c[0] for c in comments[i]],
			'tags': [t[0] for t in tags[i]],
			'author_name': authors[i][0],
			'author_pic': authors[i][1]
			})

print time.time()-start

conn.commit()
cur.close()
conn.close()
