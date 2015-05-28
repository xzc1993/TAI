from django.db import models

class User(models.Model):
	username = models.CharField(max_length=64)
	access_token = models.CharField(max_length=64)
	access_token_secret = models.CharField(max_length=64)

class Event(models.Model):
	user = models.ForeignKey(User)
	tag = models.CharField(max_length=16)
	content = models.CharField(max_length=255)
	created = models.DateTimeField( auto_now=True)

class Comment(models.Model):
	user = models.ForeignKey(User)
	event = models.ForeignKey(Event)
	content = models.CharField(max_length=255)
	created = models.DateTimeField( auto_now=True)
