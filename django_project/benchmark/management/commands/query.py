from django.core.management.base import BaseCommand, CommandError
from benchmark.models import *
import random
import time
import sys

class Command(BaseCommand): 
	# this is a sample of what the query method could be, not really sure of what it should be
	help = "Simulates showing all posts(+ comment bodies and author name) for all tags"

	def handle(self, *args, **options):
		tags = Tag.objects.all()

		# put tags in random order
		rtags = random.sample(tags, len(tags))

		start = time.time()
		
		for tag in rtags: 

			# query for tag posts
			posts = Post.objects.filter(tags__pk=tag.pk)

			# query for post comments
			comments = [[comment.body for comment in Comment.objects.filter(post=post)] for post in posts]

			# get posts' author's names
			authors = [post.author for post in posts]

			# get posts' tags names
			tags = [[tag.name for tag in post.tags] for post in posts]

			# to check that we have everything we need
			out = []
			for i in range(len(posts)): 
				out.append({
					'body': posts[i].body,
					'author_name': authors[i].name,
					'author_pic': authors[i].picture,
					'comments': comments[i],
					'tags': tags[i]
					})

		print time.time()-start