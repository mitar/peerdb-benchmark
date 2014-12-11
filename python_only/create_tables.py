# 2nd answer for virtualenv 
# http://stackoverflow.com/questions/20170895/mac-virtualenv-pip-postgresql-error-pg-config-executable-not-found
import psycopg2
import config

conn = psycopg2.connect(config.DATABASE_INFO)
cur = conn.cursor()

print "Droping tables if they exist" 
cur.execute("DROP TABLE IF EXISTS comment;")
cur.execute("DROP TABLE IF EXISTS post_tag;")
cur.execute("DROP TABLE IF EXISTS post;")
cur.execute("DROP TABLE IF EXISTS tag;")
cur.execute("DROP TABLE IF EXISTS person;")

print "Creating tables"
# create person table
cur.execute("CREATE TABLE person (person_id serial PRIMARY KEY, name text, bio text, picture text);")

# create tag table
cur.execute("CREATE TABLE tag (tag_id serial PRIMARY KEY, name VARCHAR(255), description text);")
cur.execute("CREATE INDEX ON tag (name);")

# create post table
cur.execute("CREATE TABLE post (post_id serial PRIMARY KEY, \
	body text, \
	author integer REFERENCES person (person_id));")

# create post_tag table
# http://stackoverflow.com/questions/9789736/how-to-implement-a-many-to-many-relationship-in-postgresql
cur.execute("CREATE TABLE post_tag (post_id integer REFERENCES post (post_id) ON UPDATE CASCADE ON DELETE CASCADE,\
	tag_id integer REFERENCES tag (tag_id) ON UPDATE CASCADE,\
	CONSTRAINT post_tag_pkey PRIMARY KEY (post_id, tag_id));")

# create comment table
cur.execute("CREATE TABLE comment (comment_id serial PRIMARY KEY,\
	body text,\
	post integer REFERENCES post (post_id) )")

conn.commit()
cur.close()
conn.close()
