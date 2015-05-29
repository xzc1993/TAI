import json
from django.db import models
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist

from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from threading import Lock

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

class TwitterDAO(models.Model):

	mutex = Lock()
	class NewEventListener(StreamListener):
		def on_data(self, data):
			try:
				data = json.loads(data)
				username = data['user']['screen_name']
				user = User.objects.get(username=username)
				content = data['text']
				created = data['created_at']
				hashtags = data['entities']['hashtags']
				tag = None
				for hashtag in hashtags:
					if hashtag['text'] != 'krzieba_TAI':
						tag = '#' + hashtag['text']
						break
				print tag
				try:
					event = Event.objects.get(tag=tag)
					print 'Duplicated event tag...', tag
					return True
				except ObjectDoesNotExist:
					pass
				event = Event(user=user, tag=tag, content=content.replace('#krzieba_TAI', '').replace( tag, '') , created=created)
				print 'Saving...' 	
				event.save()
				TwitterDAO.updateCommentListener()
				return True
			except Exception as e:
				print e
				print 'Received malformed status in NewEventListener'
				return True

		def on_error(self, status):
			print(status)

	class NewCommentListener(StreamListener):
		def on_data(self, data):
			try:
				data = json.loads(data)
				username = data['user']['screen_name']

				content = data['text']
				created = data['created_at']
				hashtags = data['entities']['hashtags']
				tag = '#' + hashtags[0]['text']

				user = User.objects.get(username=username)
				event = Event.objects.get(tag=tag)

				comment = Comment(user=user, event=event, content=content.replace( tag, ''), created=created)
				print 'Saving...' 	
				comment.save()
				return True
			except Exception as e:
				print e
				print 'Received malformed status in NewCommentListener'
				return True

		def on_error(self, status):
			print(status)

	@staticmethod
	def start():
		auth = OAuthHandler( settings.TWITTER_CONSUMER_KEY, settings.TWITTER_CONSUMER_SECRET)
		auth.set_access_token( settings.TWITTER_ACCESS_TOKEN, settings.TWITTER_ACCESS_TOKEN_SECRET)

		unique_tags = list(set([ event.tag for event in Event.objects.all()]))

		print unique_tags
		TwitterDAO.streamComment = Stream( auth, TwitterDAO.NewCommentListener())
		TwitterDAO.streamComment.filter(track=unique_tags, async=True)

		TwitterDAO.streamEvent = Stream(auth, TwitterDAO.NewEventListener())
		TwitterDAO.streamEvent.filter(track=['krzieba_TAI'], async=True)

	@staticmethod 
	def updateCommentListener():
		auth = OAuthHandler( settings.TWITTER_CONSUMER_KEY, settings.TWITTER_CONSUMER_SECRET)
		auth.set_access_token( settings.TWITTER_ACCESS_TOKEN, settings.TWITTER_ACCESS_TOKEN_SECRET)

		#TwitterDAO.streamComment.disconnect()
		unique_tags = list(set([ event.tag for event in Event.objects.all()]))
		print unique_tags
		TwitterDAO.streamComment = Stream( auth, TwitterDAO.NewCommentListener())
		TwitterDAO.streamComment.filter(track=unique_tags, async=True)	