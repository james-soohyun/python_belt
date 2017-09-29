# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect

from django.contrib import messages

from ..login_app.models import *

# Create your views here.

def index(request):
	if 'email' not in request.session:
		return redirect('/main')
	user = User.objects.get(id = request.session['id'])
	context = {
		"otherUsers": User.objects.exclude(id = request.session['id']),
		"users": User.objects.all(),
		"pokes": Poke.objects.filter(receive_user = user)
	}
	poke = Poke.objects.filter(receive_user = user)
	for user in poke:
		print user.send_user.name
	return render(request, 'poke_app/index.html', context)

def logout(request):
	request.session.flush()
	return redirect('/main')

def poke(request, user_id):
	if 'email' not in request.session:
		return redirect('/main')
	user = User.objects.get(id = request.session['id'])
	receiver = User.objects.get(id = user_id)
	Poke.objects.create(send_user = user, receive_user = receiver)
	return redirect('/pokes')