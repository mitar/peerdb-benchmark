from django.core.management.base import BaseCommand
from benchmark.models import *
import time

class Command(BaseCommand): 
	help = "Query and benchmark the database"

	def handle(self, *args, **options):
		self.stderr.write("Checking collection counts\n")

		persons_count = Person.objects.all().count()
		tags_count = Tag.objects.all().count()
		posts_count = Post.objects.all().count()
		comments_count = Comment.objects.all().count()

		self.stderr.write(' '.join(["Persons:", str(persons_count), "Tags:", str(tags_count),
		"Posts:", str(posts_count), "Comments:", str(comments_count)]) + '\n')

		self.stderr.write("Querying all posts and content for each tag\n")

		start = time.time()

		# iterate over all tags
		# we pretend that tag name is the only thing we have to begin with
		for cur_tag_name in Tag.objects.all().values_list('name', flat=True):
			tp_contents = []
			# TODO: Is this really the best we can do? It is still 10x slower than manual query.
			for post in Post.objects.filter(tags__name__exact=cur_tag_name).select_related('author').prefetch_related('tags', 'comments'):
				tp_contents.append({
					'body': post.body,
					'comments': [comment.body for comment in post.comments.all()],
					'author_name': post.author.name,
					'author_picture': post.author.picture,
					'tags_name': [tag.name for tag in post.tags.all()],
					'tags_description': [tag.description for tag in post.tags.all()]
					})

		self.stdout.write(str(time.time()-start)+"\n")
