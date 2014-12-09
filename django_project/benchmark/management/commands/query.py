from django.core.management.base import BaseCommand, CommandError
from benchmark.models import *
import random

class Command(BaseCommand): 
	# this is a sample of what the query method could be, not really sure of what it should be
	help = "Simulates showing all posts(+ comment bodies and author name) for all tags"

	def handle(self, *args, **options):
		tags = Tag.objects.all()

		# put tags in random order
		rtags = random.sample(tags, len(tags))

		count = 0
		for tag in rtags: 

			# get posts for that tag
			posts = Post.objects.filter(tags__pk=tag.pk)

			# for each post get body
			post_bodies = [post.body for post in posts]

			# for each post get all comment bodies
			comments = [[comment.body for comment in Comment.objects.filter(post=post)] for post in posts]

			# for each post get author name
			authors = [post.author.name for post in posts]

			count+=1
			if count%10 == 0: print "Done with",count,"tags"