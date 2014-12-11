from django.core.management.base import BaseCommand, CommandError
from benchmark.models import *
import random
import json
import string
import sys
import time

class Command(BaseCommand): 
	help = "populates database according to populate.coffee"

	def handle(self, *args, **options):

		def char_generator(size=6, chars=string.ascii_uppercase + string.digits):
			return ''.join(random.choice(chars) for _ in range(size))

		sys.stderr.write("Setting parameters\n")
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
		
		sys.stderr.write("Cleaning the database\n")

		Comment.objects.all().delete()
		Post.objects.all().delete()
		Tag.objects.all().delete()
		Person.objects.all().delete()

		sys.stderr.write("Done\n")

		sys.stderr.write("Adding "+str(NUMBER_OF_PERSONS)+" persons\n")

		start = time.time()

		for i in range(NUMBER_OF_PERSONS): 
			person = Person(name=PERSON_NAME, picture=PERSON_PICTURE, bio=PERSON_BIO)
			person.save()

		sys.stderr.write("Adding "+str(NUMBER_OF_TAGS)+" tags\n")

		for i in range(NUMBER_OF_TAGS): 
			tag = Tag(name=TAG_NAME, description=TAG_DESCRIPTION)
			tag.save()

		sys.stderr.write("Adding "+str(NUMBER_OF_POSTS)+" posts\n")

		persons = Person.objects.all()
		tags = Tag.objects.all()
		for i in range(NUMBER_OF_POSTS): 
			post = Post(author=random.choice(persons), body=POST_BODY)
			# has to have primary key before creating many-to-many
			post.save()

			# adding randomly sampled tags to the post
			rtags = random.sample(tags, NUMBER_OF_TAGS_PER_POST)
			for tag in rtags: 
				post.tags.add(tag)

			# saving post after tags added
			post.save()

		sys.stderr.write("Adding "+str(NUMBER_OF_COMMENTS)+" comments\n")


		posts = Post.objects.all()
		for i in range(NUMBER_OF_COMMENTS): 
			comment = Comment(body=COMMENT_BODY, post=random.choice(posts))
			comment.save()
		sys.stderr.write("Done\n")

		print time.time() - start
		
			


