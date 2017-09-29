# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

import bcrypt

import re

# Create your models here.

class UserManager(models.Manager):
	def validate(self, postData):
		results = {
			'status': True,
			'errors': []
		}
		if len(postData['name']) < 3:
			results['errors'].append('Name is too short')
			results['status'] = False
		if len(postData['alias']) < 3:
			results['errors'].append('Alias is too short')
			results['status'] = False
		if not re.match("[^@]+@[^@]+\.[^@]+", postData['email']):
			results['errors'].append('Email is not valid')
			results['status'] = False
		if postData['password'] != postData['confirm']:
			results['errors'].append('Passwords do not match')
			results['status'] = False
		if len(postData['password']) < 8:
			results['errors'].append('Password is too short')
			results['status'] = False
		if len(postData['birthday']) <1:
			results['errors'].append('Please enter birthday')
			results['status'] = False
		if len(self.filter(email = postData['email'])) > 0:
			results['errors'].append('User already exists')
			results['status'] = False
		return results

	def creator(self, postData):
		user = self.create(name = postData['name'], alias = postData['alias'], email = postData['email'], password = bcrypt.hashpw(postData['password'].encode(), bcrypt.gensalt()), birthday = postData['birthday'])
		return user

	def loginVal(self, postData):
		results = {
			'status': True,
			'errors': [],
			'user': None
		}
		users = self.filter(email = postData['email'])
		if len(users) <1:
			results['status'] = False
		else:
			if bcrypt.checkpw(postData['password'].encode(), users[0].password.encode()):
				results['user'] = users[0]
			else:
				results['status'] = False
		return results

class User(models.Model):
	name = models.CharField(max_length = 200)
	alias = models.CharField(max_length = 200)
	email = models.CharField(max_length = 200)
	password = models.CharField(max_length = 200)
	birthday = models.CharField(max_length = 10)
	created_at = models.DateTimeField(auto_now_add = True)
	updated_at = models.DateTimeField(auto_now = True)
	objects = UserManager()

class Poke(models.Model):
	send_user = models.ForeignKey(User, related_name = "poker")
	receive_user = models.ForeignKey(User, related_name = "pokee")
