# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect

from models import User, Poke

from django.contrib import messages

# Create your views here.

def index(request):
	return render(request, 'login_app/index.html')

def register(request):

	results = User.objects.validate(request.POST)

	if results['status'] == True:
		user = User.objects.creator(request.POST)
		messages.success(request, 'Registration successful')

	else:
		for error in results['errors']:
			messages.error(request, error)

	return redirect('/main')

def login(request):
	results = User.objects.loginVal(request.POST)
	if results['status'] == False:
		messages.error(request, 'Email/password is invalid')
		return redirect('/main')
	request.session['email'] = results['user'].email
	request.session['name'] = results['user'].name
	request.session['alias'] = results['user'].alias
	request.session['birthday'] = results['user'].birthday
	request.session['id'] = results['user'].id
	return redirect('/main/directory')

def directory(request):
	if 'email' not in request.session:
		return redirect('/main')
	return redirect('/pokes')