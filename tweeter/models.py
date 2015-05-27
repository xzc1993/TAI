from django.db import models

class User(models.Model):
	username = models.CharField(max_length=64)
	access_token = models.CharField(max_length=64)
	access_token_secret = models.CharField(max_length=64)


# Create your models here.
