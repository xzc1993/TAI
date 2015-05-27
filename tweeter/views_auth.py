from django.shortcuts import render, redirect
from django.http import HttpResponse
import tweepy
from pprint import pprint
from models import User
from  django.core.exceptions import ObjectDoesNotExist
from django.conf import settings

def test(request, *args, **kwargs):
	return render(request, 'base.html')
	
def register(request, **kwargs):
	auth = tweepy.OAuthHandler( settings.TWITTER_CONSUMER_KEY,  settings.TWITTER_CONSUMER_SECRET, 'http://127.0.0.1:8000/auth/register2')
	auth.secure = True
	authorization_url = auth.get_authorization_url()
	request.session['token'] = auth.request_token
	return redirect( authorization_url)

def register2(request, **kwargs):
	verifier = request.REQUEST['oauth_verifier']
	auth = tweepy.OAuthHandler( settings.TWITTER_CONSUMER_KEY,  settings.TWITTER_CONSUMER_SECRET)
	auth.request_token = request.session['token']
	del request.session['token']
	try:
	    auth.get_access_token(verifier)
	except tweepy.TweepError:
	    raise
	api = tweepy.API(auth)

	response = str()
	username = api.me().screen_name
	try:
		user = User.objects.get(username = username)
		user.access_token = auth.access_token
		user.access_token_secret = auth.access_token_secret
		response = "Updated"
	except ObjectDoesNotExist:
		user = User(username = username, access_token=auth.access_token, access_token_secret=auth.access_token_secret)
		response = "Created"
	user.save()
	addUserDataToSession( request, user)
	return HttpResponse( response + " " + username )

def login(request, redirectTo=None,**kwargs):
	username = request.REQUEST.get('username', None)
	if username:
		try:
			user = User.objects.get(username = username)
			addUserDataToSession( request, user)	
			if redirectTo:
				redirect( redirectTo)
			else:
				redirect( 'main')
		except ObjectDoesNotExist:
			return HttpResponse( username + " does not exists")
	return HttpResponse("Request does not contain field 'username'")

def logout(request, **kwargs):
	removeUserDataFromSession()
	return HttpResponse("Logged out")

def ensureUserLoggedIn( fun ):
	def f(request, *args, **kwargs):
		if isUserLoggedIn(request):
			return f( request, *args, **kwargs)
		else:
			redirect( 'login', redirectTo=request.path)

def isUserLoggedIn(request):
	if 'username' in request.session:
		return True
	return False

def addUserDataToSession(request, user):
	request.session['username'] = user.username
	request.session['access_token'] = user.access_token
	request.session['access_token_secret'] = user.access_token_secret	

def removeUserDataFromSession(request):
	del request.session['username']
	del request.session['access_token']
	del request.session['access_token_secret']	