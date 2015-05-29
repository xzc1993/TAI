"""
WSGI config for zieba_krzysztof_TAI project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/howto/deployment/wsgi/
"""

import os, json, django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "zieba_krzysztof_TAI.settings")
django.setup()

from django.core.wsgi import get_wsgi_application
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist

from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from pprint import pprint
from twitter.models import Event, User, Comment, TwitterDAO

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
			return True
		except:
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

application = get_wsgi_application()

TwitterDAO.start()




