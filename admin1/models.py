from django.db import models
from django.shortcuts import render , redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.contrib import auth
from django.utils import timezone


class add_project(models.Model):
	id = models.AutoField
	user_id = models.ForeignKey(User, default="0", on_delete=models.CASCADE)
	projectname = models.CharField(max_length=35, default="0")
	description = models.CharField(max_length=35, default="0")
	start_time = models.DateTimeField(default="")
	end_time = models.DateTimeField(default="")
	amount = models.IntegerField(default="0")
	front_end = models.CharField(max_length=30, default="")
	back_end = models.CharField(max_length=30, default="")
	status = models.CharField(max_length=20, default="")
	create_at = models.DateTimeField(default=timezone.now)
	updated_at = models.DateTimeField(default=timezone.now)
	def __str__(self):
		return self.projectname
