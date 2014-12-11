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

start = time.time()
# iterate over all tags
tags_cur.execute("""SELECT name from tag""")
# we pretend that tag name is the only thing we have to begin with
for (cur_tag_name,) in tags_cur:
	# query to get posts that include current tag
	# making sure I got all info for each post
	# make a list of dicts where each dict contains post contents
	cur.execute("""
		SELECT post.post_id, post.body, person.name, person.picture, tag.tag_id, tag.name, tag.description, comment.comment_id, comment.body
		FROM post
		INNER JOIN person ON (post.author = person.person_id)
		LEFT JOIN post_tag ON (post.post_id = post_tag.post_id)
		INNER JOIN tag ON (post_tag.tag_id = tag.tag_id)
		LEFT JOIN comment ON (post.post_id = comment.post)
		WHERE post.post_id IN (
			SELECT post.post_id
			FROM post
			INNER JOIN post_tag ON (post.post_id = post_tag.post_id)
			INNER JOIN tag ON (post_tag.tag_id = tag.tag_id)
			WHERE tag.name = %(cur_tag_name)s
		)
	""", {'cur_tag_name': cur_tag_name})

	last_post_id = None
	seen_posts = set()
	seen_tags = set()
	seen_comments = set()

	tp_contents = []
	for (post_id, post_body, author_name, author_picture, tag_id, tag_name, tag_description, comment_id, comment_body) in cur:
		if post_id not in seen_posts:
			seen_posts.add(post_id)
			seen_tags = set()
			seen_comments = set()
			tp_contents.append({
				"body": post_body,
				"comments": [],
				"author_name": author_name,
				"author_picture": author_picture,
				"tags_name": [],
				"tags_description": []
				})
		else:
			# assumption is that rows are ordered so that all equal post_id are together
			assert last_post_id == post_id
		last_post_id = post_id

		if tag_id not in seen_tags:
			seen_tags.add(tag_id)
			tp_contents[-1]["tags_name"].append(tag_name)
			tp_contents[-1]["tags_description"].append(tag_description)

		if comment_id not in seen_comments:
			seen_comments.add(comment_id)
			tp_contents[-1]["comments"].append(comment_body)

print time.time()-start

tags_cur.close()
cur.close()
conn.close()
