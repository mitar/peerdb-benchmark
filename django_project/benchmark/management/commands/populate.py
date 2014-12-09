from django.core.management.base import BaseCommand, CommandError
from benchmark.models import *
import random

class Command(BaseCommand): 
	help = "populates database according to populate.coffee"

	def handle(self, *args, **options):

		print "Cleaning the database"

		Comment.objects.all().delete()
		Post.objects.all().delete()
		Tag.objects.all().delete()
		Person.objects.all().delete()

		print "Done"

		# same as https://github.com/mitar/peerdb-benchmark/
		# blob/mongodb-meteor/server/populate.coffee
		NUMBER_OF_PERSONS = 100
		NUMBER_OF_TAGS = 100
		NUMBER_OF_POSTS = 1000
		NUMBER_OF_TAGS_PER_POST = 10
		NUMBER_OF_COMMENTS = 10000

		print "Adding", NUMBER_OF_PERSONS, "persons"

		for i in range(NUMBER_OF_PERSONS): 
			person = Person(name="name", picture="picture", bio="bio")
			person.save()

		print "Adding", NUMBER_OF_TAGS, "tags"

		for i in range(NUMBER_OF_TAGS): 
			tag = Tag(name="name", description="description")
			tag.save()

		print "Adding", NUMBER_OF_POSTS,"posts"

		persons = Person.objects.all()
		tags = Tag.objects.all()
		for i in range(NUMBER_OF_POSTS): 
			post = Post(author=random.choice(persons), body="body")
			# has to have primary key before creating many-to-many
			post.save()

			# adding randomly sampled tags to the post
			rtags = random.sample(tags, NUMBER_OF_TAGS_PER_POST)
			for tag in rtags: 
				post.tags.add(tag)

			# saving post after tags added
			post.save()

		print "Adding", NUMBER_OF_COMMENTS, "comments"

		posts = Post.objects.all()
		for i in range(NUMBER_OF_COMMENTS): 
			comment = Comment(body="body", post=random.choice(posts))
			comment.save()

		print "Done"
			


