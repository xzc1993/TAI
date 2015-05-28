import tweepy

from models import Event, User, Comment

from django.shortcuts import render, redirect
from django.conf import settings
from django.forms import ModelForm

from helper_auth import ensureUserLoggedIn

class EventForm(ModelForm):
    class Meta:
        model = Event
        fields = ['tag', 'content']

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['content']

def main(request, *args, **kwargs):
	return render(request, 'base.html')

@ensureUserLoggedIn
def events(request, *args, **kwargs):
	events = Event.objects.all()
	return render( request, 'events.html', {'events' : events})

@ensureUserLoggedIn
def newEvent(request, *args, **kwargs):
	form = EventForm()
	return render( request, 'newEvent.html', {'form': form})

@ensureUserLoggedIn
def createEvent(request, *args, **kwargs):
	form = EventForm(request.REQUEST)
	event = form.save(commit=False)
	event.user_id = User.objects.get(username=request.session['username']).id
	event.tag = '#' + event.tag
	auth = tweepy.OAuthHandler( settings.TWITTER_CONSUMER_KEY,  settings.TWITTER_CONSUMER_SECRET)
	auth.access_token = request.session['access_token']
	auth.access_token_secret = request.session['access_token_secret']
	api = tweepy.API(auth)
	api.update_status( status= (event.tag + '\n' + event.content))
	event.save()
	return redirect('events')

@ensureUserLoggedIn
def showEvent(request, *args, **kwargs):
	form = EventForm( instance=Event.objects.get(pk=kwargs['event_id']))
	comments = Comment.objects.filter(event_id=kwargs['event_id'])
	return render( request, 'showEvent.html', {'form': form, 'event_id': kwargs['event_id'], 'comments': comments})

@ensureUserLoggedIn
def newComment(request, *args, **kwargs):
	form = CommentForm()
	return render( request, 'newComment.html', {'form': form, 'event_id': kwargs['event_id']})

@ensureUserLoggedIn
def createComment(request, *args, **kwargs):
	form = CommentForm(request.REQUEST)
	comment = form.save(commit=False)
	comment.user_id = User.objects.get(username=request.session['username']).id
	comment.event_id = kwargs['event_id']
	auth = tweepy.OAuthHandler( settings.TWITTER_CONSUMER_KEY,  settings.TWITTER_CONSUMER_SECRET)
	auth.access_token = request.session['access_token']
	auth.access_token_secret = request.session['access_token_secret']
	api = tweepy.API(auth)
	api.update_status( status= (comment.event.tag + '\n' + comment.content))
	comment.save()
	return redirect('showEvent', event_id=kwargs['event_id'])
