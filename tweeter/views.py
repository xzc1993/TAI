from django.shortcuts import render, redirect
from django.http import HttpResponse
import tweepy
from pprint import pprint
from models import User
from  django.core.exceptions import ObjectDoesNotExist
from django.conf import settings

def main(request, *args, **kwargs):
	return render(request, 'base.html')