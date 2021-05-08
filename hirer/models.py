from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from admin1.models import add_project


class comment(models.Model):
	id = models.AutoField
	fname = models.CharField(max_length=35, default="0")
	lname = models.CharField(max_length=35, default="0")
	email = models.CharField(max_length=35, default="0")
	subject	 = models.CharField(max_length=35, default="0")
	message = models.CharField(max_length=1000, default="0")
	create_at = models.DateTimeField(default=timezone.now)
	updated_at = models.DateTimeField(default=timezone.now)

class project_bid_rate(models.Model):
	id = models.AutoField
	user = models.ForeignKey(User, default="", on_delete=models.CASCADE)
	project = models.CharField(default="0", max_length=50)
	bid_rate = models.IntegerField(default="0")
	comments = models.CharField(max_length=500, default="")
	status = models.CharField(max_length=50, default="")
	# last_date=models.ForeignKey(add_project, on_delete=models.CASCADE)
	progress = models.CharField(max_length=50, default="")
	create_at = models.DateTimeField(default=timezone.now)
	updated_at = models.DateTimeField(default=timezone.now)

class payment_report(models.Model):
	id = models.AutoField
	user = models.ForeignKey(User, default="", on_delete=models.CASCADE)
	project = models.CharField(max_length=50, default="0")
	total_amount = models.IntegerField(default="")
	received_amount = models.IntegerField(default="")
	create_at = models.DateTimeField(default=timezone.now)
	updated_at = models.DateTimeField(default=timezone.now)

