from django.db import models
from django.contrib.auth.models import User
from problems.models import Group


class MyUser(models.Model):
	user = models.OneToOneField(User, primary_key=True)
	motto = models.CharField(max_length=140, blank = True)
	accomplishments = models.IntegerField(default=0)

	def __str__(self):
		return str(self.user)


class Ranking(models.Model):
	group = models.ForeignKey(Group, on_delete=models.CASCADE)
	my_user = models.ForeignKey(MyUser, on_delete=models.CASCADE,default=1)
	did = models.IntegerField(default=0)