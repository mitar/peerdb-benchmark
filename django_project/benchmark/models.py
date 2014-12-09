from django.db import models

# Create your models here.
class Person(models.Model): 
	name = models.TextField()
	picture = models.TextField()
	bio = models.TextField()

class Tag(models.Model): 
	name = models.TextField()
	description = models.TextField()

class Post(models.Model): 
	author = models.ForeignKey(Person)
	tags = models.ManyToManyField(Tag)
	body = models.TextField()

class Comment(models.Model): 
	body = models.TextField()
	post = models.ForeignKey(Post)
