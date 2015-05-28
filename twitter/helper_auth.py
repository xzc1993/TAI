from django.shortcuts import render, redirect
from django.core.urlresolvers import resolve

def ensureUserLoggedIn( fun ):
	def f(request, *args, **kwargs):
		if isUserLoggedIn(request):
			return fun( request, *args, **kwargs)
		else:
			print request.path
			return redirect( 'signInWithTwitter', redirectTo= '/' + request.path)
	return f

def isUserLoggedIn(request):
	if 'username' in request.session:
		return True
	return False