import psycopg2
import random

conn=psycopg2.connect("dbname='python_db' user='apavel' password='' host='localhost'")
cur = conn.cursor()

# same as https://github.com/mitar/peerdb-benchmark/
# blob/mongodb-meteor/server/populate.coffee
NUMBER_OF_PERSONS = 100
NUMBER_OF_TAGS = 100
NUMBER_OF_POSTS = 1000
NUMBER_OF_TAGS_PER_POST = 10
NUMBER_OF_COMMENTS = 10000

print "Adding", NUMBER_OF_PERSONS, "persons"

persons = []
for person in range(NUMBER_OF_PERSONS): 
	# TODO: Add picture
	persons.append({
		"name": "name", 
		"bio": "bio"
		})
cur.executemany("""INSERT INTO person(name, bio) VALUES (%(name)s, %(bio)s)""", tuple(persons))

print "Adding", NUMBER_OF_TAGS, "tags"

tags = []
for i in range(NUMBER_OF_TAGS): 
	tags.append({
		"name": "name",
		"description": "description"
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
		'body': 'body'
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
		"body": "body",
		"post": random.choice(post_ids)
		})
cur.executemany("""INSERT INTO comment(body, post) VALUES (%(body)s, %(post)s)""", tuple(comments))

print "Done!"

conn.commit()
cur.close()
conn.close()
