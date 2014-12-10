import psycopg2
import random
import config
import sys
import json
import string

def char_generator(size=6, chars=string.ascii_uppercase + string.digits):
	return ''.join(random.choice(chars) for _ in range(size))

def main(args): 
	if not args: 
		print "Supply parameter json file: python populate.py sample_parameters.json"
		exit(-1)

	f = open(args[0])
	param = json.load(f)
	f.close()

	NUMBER_OF_PERSONS = param['NUMBER']['PERSONS']
	NUMBER_OF_TAGS = param['NUMBER']['TAGS']
	NUMBER_OF_POSTS = param['NUMBER']['POSTS']
	NUMBER_OF_TAGS_PER_POST = param['NUMBER']['TAGS_PER_POST']
	NUMBER_OF_COMMENTS = param['NUMBER']['COMMENTS']

	PERSON_NAME = char_generator(param['SIZE']['PERSON_NAME'])
	PERSON_BIO = char_generator(param['SIZE']['PERSON_BIO'])
	PERSON_PICTURE = char_generator(param['SIZE']['PERSON_PICTURE'])
	TAG_NAME = char_generator(param['SIZE']['TAG_NAME'])
	TAG_DESCRIPTION = char_generator(param['SIZE']['TAG_DESCRIPTION'])
	POST_BODY = char_generator(param['SIZE']['POST_BODY'])
	COMMENT_BODY = char_generator(param['SIZE']['COMMENT_BODY'])

	conn=psycopg2.connect(config.DATABASE_INFO)
	cur = conn.cursor()
	
	print "Adding", NUMBER_OF_PERSONS, "persons"

	persons = []
	for person in range(NUMBER_OF_PERSONS): 
		# TODO: Add picture
		persons.append({
			"name": PERSON_NAME, 
			"bio": PERSON_BIO,
			"picture": PERSON_PICTURE
			})
	cur.executemany("""INSERT INTO person(name, bio, picture) VALUES (%(name)s, %(bio)s, %(picture)s)""", tuple(persons))

	print "Adding", NUMBER_OF_TAGS, "tags"

	tags = []
	for i in range(NUMBER_OF_TAGS): 
		tags.append({
			"name": TAG_NAME,
			"description": TAG_DESCRIPTION
			})
	cur.executemany("""INSERT INTO tag(name, description) VALUES (%(name)s, %(description)s)""", tuple(tags))

	print "Getting person ID's so far" 
	cur.execute("""SELECT person_id from person""")
	person_ids = cur.fetchall()
	print "First 5 person ID's", person_ids[:5]

	print "Getting tag ID's so far" 
	cur.execute("""SELECT tag_id from tag""")
	tag_ids = cur.fetchall()
	print "First 5 tag ID's", tag_ids[:5]

	print "Adding", NUMBER_OF_POSTS,"posts"

	posts = []
	for i in range(NUMBER_OF_POSTS): 
		posts.append({
			'author': random.choice(person_ids),
			'body': POST_BODY
			})
	cur.executemany("""INSERT INTO post(author, body) VALUES (%(author)s, %(body)s)""", tuple(posts))

	print "Getting post ID's so far" 
	cur.execute("""SELECT post_id from post""")
	post_ids = cur.fetchall()
	print "First 5 post ID's", post_ids[:5]

	print "Adding", NUMBER_OF_TAGS_PER_POST, "tags per post"

	post_tags = []
	for post_id in post_ids: 
		tag_sample = random.sample(tag_ids, NUMBER_OF_TAGS_PER_POST)

		for tag_id in tag_sample: 
			post_tags.append({
				'post_id': post_id, 
				'tag_id': tag_id
				})
	cur.executemany("""INSERT INTO post_tag(post_id, tag_id) VALUES (%(post_id)s, %(tag_id)s)""", tuple(post_tags))

	print "Adding", NUMBER_OF_COMMENTS, "comments"

	comments = []
	for i in range(NUMBER_OF_COMMENTS): 
		comments.append({
			"body": COMMENT_BODY,
			"post": random.choice(post_ids)
			})
	cur.executemany("""INSERT INTO comment(body, post) VALUES (%(body)s, %(post)s)""", tuple(comments))

	print "Done!"

	conn.commit()
	cur.close()
	conn.close()


if __name__ == '__main__':
	main(sys.argv[1:])


