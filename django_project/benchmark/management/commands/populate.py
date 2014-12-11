from django.core.management.base import BaseCommand, CommandError
from benchmark.models import *
import random
import json
import string
import time

def char_generator(size=6, chars=string.ascii_uppercase + string.digits):
	return ''.join(random.choice(chars) for _ in range(size))

class Command(BaseCommand): 
	help = "Populates the database."

	def handle(self, *args, **options):
		if not args:
			raise CommandError("Supply parameter json file")

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

		self.stderr.write("Cleaning the database\n")

		Comment.objects.all().delete()
		Post.objects.all().delete()
		Tag.objects.all().delete()
		Person.objects.all().delete()

		self.stderr.write("Done\n")

		self.stderr.write("Adding "+str(NUMBER_OF_PERSONS)+" persons\n")

		start = time.time()

		persons = []
		for i in range(NUMBER_OF_PERSONS):
			persons.append(Person(
				name=char_generator(PERSON_NAME_SIZE),
				picture=char_generator(PERSON_BIO_SIZE),
				bio=char_generator(PERSON_PICTURE_SIZE)
				))
		Person.objects.bulk_create(persons)

		self.stderr.write("Adding "+str(NUMBER_OF_TAGS)+" tags\n")

		tags = []
		for i in range(NUMBER_OF_TAGS):
			tags.append(Tag(
				name=char_generator(TAG_NAME_SIZE),
				description=char_generator(TAG_DESCRIPTION_SIZE)
				))
		Tag.objects.bulk_create(tags)

		self.stderr.write("Getting person ID's so far\n")

		person_ids = Person.objects.all().values_list('id', flat=True)

		self.stderr.write("Getting tag ID's so far\n")

		tag_ids = Tag.objects.all().values_list('id', flat=True)

		self.stderr.write("Adding "+str(NUMBER_OF_POSTS)+" posts\n")

		posts = []
		for i in range(NUMBER_OF_POSTS):
			posts.append(Post(
				author_id=random.choice(person_ids),
				body=char_generator(POST_BODY_SIZE)
				))
		Post.objects.bulk_create(posts)

		post_ids = []

		self.stderr.write("Adding "+str(NUMBER_OF_TAGS_PER_POST)+" tags per post\n")

		for post in Post.objects.all().only('id'):
			post_ids.append(post.id)

			# adding randomly sampled tags to the post
			tag_sample = random.sample(tag_ids, NUMBER_OF_TAGS_PER_POST)

			for tag_id in tag_sample:
				post.tags.add(tag_id)

			# saving post after tags added
			post.save()

		assert len(post_ids) == len(posts)

		self.stderr.write("Adding "+str(NUMBER_OF_COMMENTS)+" comments\n")

		comments = []
		for i in range(NUMBER_OF_COMMENTS):
			comments.append(Comment(
				body=char_generator(COMMENT_BODY_SIZE),
				# TODO: We should use here some long-tail distribution (20% of posts has 80% of comments)
				post_id=random.choice(post_ids)
				))
		Comment.objects.bulk_create(comments)

		#self.stderr.write("Getting comment ID's so far\n")

		#comment_ids = Comment.objects.all().values_list('id', flat=True)

		self.stdout.write(str(time.time()-start)+"\n")
