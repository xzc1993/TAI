import tweepy

from models import User

from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
from django.core.urlresolvers import reverse, resolve
from django.http import Http404	

def signInWithTwitter(request, **kwargs):
	auth = tweepy.OAuthHandler( settings.TWITTER_CONSUMER_KEY,  settings.TWITTER_CONSUMER_SECRET, 'http://127.0.0.1:8000/auth/signInWithTwitter2')
	auth.secure = True
	authorization_url = auth.get_authorization_url( signin_with_twitter=True)
	request.session['token'] = auth.request_token
	return redirect( authorization_url)

def signInWithTwitter2(request, **kwargs):
	verifier = request.REQUEST['oauth_verifier']
	auth = tweepy.OAuthHandler( settings.TWITTER_CONSUMER_KEY,  settings.TWITTER_CONSUMER_SECRET)
	auth.request_token = request.session['token']
	del request.session['token']
	try:
	    auth.get_access_token(verifier)
	except tweepy.TweepError:
	    raise
	api = tweepy.API(auth)

	username = api.me().screen_name
	try:
		user = User.objects.get(username = username)
		user.access_token = auth.access_token
		user.access_token_secret = auth.access_token_secret
	except ObjectDoesNotExist:
		user = User(username = username, access_token=auth.access_token, access_token_secret=auth.access_token_secret)
	user.save()
	addUserDataToSession( request, user)
	redirectTo = request.session.get('redirectTo', 'main')
	if 'redirectTo' in request.session:
		del request.session['redirectTo']
	try:
		match = resolve( redirectTo)
		return redirect( match.url_name, *(match.args), **(match.kwargs))
	except Http404:
		return redirect( redirectTo )

def logout(request, *args, **kwargs):
	removeUserDataFromSession(request)
	return redirect( 'main')

def addUserDataToSession(request, user):
	request.session['username'] = user.username
	request.session['access_token'] = user.access_token
	request.session['access_token_secret'] = user.access_token_secret	

def removeUserDataFromSession(request):
	del request.session['username']
	del request.session['access_token']
	del request.session['access_token_secret']	