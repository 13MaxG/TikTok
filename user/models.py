from django.db import models
from django.contrib.auth.models import User


class MyUser(models.Model):
	user = models.OneToOneField(User, primary_key=True)
	motto = models.CharField(max_length=140, blank = True)
	accomplishments = models.IntegerField(default=0)

	def __str__(self):
		return str(self.user)
