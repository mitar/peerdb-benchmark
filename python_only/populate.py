import psycopg2
import random
import config
import sys
import json
import string
import time

def char_generator(size=6, chars=string.ascii_uppercase + string.digits):
	return ''.join(random.choice(chars) for _ in range(size))

def main(args): 
	if not args: 
		sys.stderr.write("Supply parameter json file\n")
		exit(-1)

	f = open(args[0])
	param = json.load(f)
	f.close()

	NUMBER_OF_PERSONS = param['NUMBER']['PERSONS']
	NUMBER_OF_TAGS = param['NUMBER']['TAGS']
	NUMBER_OF_POSTS = param['NUMBER']['POSTS']
	NUMBER_OF_TAGS_PER_POST = param['NUMBER']['TAGS_PER_POST']
	NUMBER_OF_COMMENTS = param['NUMBER']['COMMENTS']

	PERSON_NAME_SIZE = param['SIZE']['PERSON_NAME']
	PERSON_BIO_SIZE = param['SIZE']['PERSON_BIO']
	PERSON_PICTURE_SIZE = param['SIZE']['PERSON_PICTURE']
	TAG_NAME_SIZE = param['SIZE']['TAG_NAME']
	TAG_DESCRIPTION_SIZE = param['SIZE']['TAG_DESCRIPTION']
	POST_BODY_SIZE = param['SIZE']['POST_BODY']
	COMMENT_BODY_SIZE = param['SIZE']['COMMENT_BODY']

	conn = psycopg2.connect(config.DATABASE_INFO)
	cur = conn.cursor()
	
	sys.stderr.write("Adding "+str(NUMBER_OF_PERSONS)+" persons\n")

	start = time.time()
	persons = []
	for i in range(NUMBER_OF_PERSONS):
		persons.append({
			"name": char_generator(PERSON_NAME_SIZE),
			"bio": char_generator(PERSON_BIO_SIZE),
			"picture": char_generator(PERSON_PICTURE_SIZE)
			})
	cur.executemany("""INSERT INTO person(name, bio, picture) VALUES (%(name)s, %(bio)s, %(picture)s)""", persons)

	sys.stderr.write("Adding "+str(NUMBER_OF_TAGS)+" tags\n")

	tags = []
	for i in range(NUMBER_OF_TAGS): 
		tags.append({
			"name": char_generator(TAG_NAME_SIZE),
			"description": char_generator(TAG_DESCRIPTION_SIZE)
			})
	cur.executemany("""INSERT INTO tag(name, description) VALUES (%(name)s, %(description)s)""", tags)

	sys.stderr.write("Getting person ID's so far\n")
	cur.execute("""SELECT person_id from person""")
	person_ids = cur.fetchall()

	sys.stderr.write("Getting tag ID's so far\n")
	cur.execute("""SELECT tag_id from tag""")
	tag_ids = cur.fetchall()

	sys.stderr.write("Adding "+str(NUMBER_OF_POSTS)+" posts\n")

	posts = []
	for i in range(NUMBER_OF_POSTS): 
		posts.append({
			'author': random.choice(person_ids),
			'body': char_generator(POST_BODY_SIZE)
			})
	cur.executemany("""INSERT INTO post(author, body) VALUES (%(author)s, %(body)s)""", posts)

	sys.stderr.write("Getting post ID's so far\n")
	cur.execute("""SELECT post_id from post""")
	post_ids = cur.fetchall()

	sys.stderr.write("Adding "+str(NUMBER_OF_TAGS_PER_POST)+" tags per post\n")

	post_tags = []
	for post_id in post_ids: 
		tag_sample = random.sample(tag_ids, NUMBER_OF_TAGS_PER_POST)

		for tag_id in tag_sample: 
			post_tags.append({
				'post_id': post_id, 
				'tag_id': tag_id
				})
	cur.executemany("""INSERT INTO post_tag(post_id, tag_id) VALUES (%(post_id)s, %(tag_id)s)""", post_tags)

	sys.stderr.write("Adding "+str(NUMBER_OF_COMMENTS)+" comments\n")

	comments = []
	for i in range(NUMBER_OF_COMMENTS): 
		comments.append({
			"body": char_generator(COMMENT_BODY_SIZE),
			# TODO: We should use here some long-tail distribution (20% of posts has 80% of comments)
			"post": random.choice(post_ids)
			})
	cur.executemany("""INSERT INTO comment(body, post) VALUES (%(body)s, %(post)s)""", comments)

	print time.time()-start

	# sys.stderr.write("Getting comment ID's so far\n")
	# cur.execute("""SELECT comment_id from comment""")
	# comment_ids = cur.fetchall()

	conn.commit()
	cur.close()
	conn.close()

if __name__ == '__main__':
	main(sys.argv[1:])
