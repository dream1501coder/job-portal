from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from admin1.models import add_project
# Create your models here.

class profile(models.Model):
	id = models.AutoField
	user_id = models.OneToOneField(User, default="0", on_delete=models.CASCADE)
	phonenumber = models.IntegerField(default="0")
	address = models.CharField(max_length=35,default="0")
	technology = models.CharField(max_length=35,default="0")
	image = models.ImageField(default="")
	status = models.CharField(max_length=35,default="0")
	is_login = models.CharField(default="", max_length=35)
	create_at = models.DateTimeField(default=timezone.now)
	updated_at = models.DateTimeField(default=timezone.now)
	def __str__(self):
		return self.user_id.username


