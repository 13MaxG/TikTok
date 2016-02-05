from django.db import models
from django.contrib.auth.models import User

class Problem(models.Model):
	name = models.CharField(default='', max_length=255)
	user = models.ForeignKey(User, default=1, null=True)
	pdf_file_link = models.CharField(default='', max_length=255)
	pub_date = models.DateTimeField('date published')
	users_total = models.IntegerField(default=0)
	users_did = models.IntegerField(default=0)

	def __str__(self):
		return self.name


class TestProgram(models.Model):
	problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
	code = models.TextField(default='')
	time = models.FloatField(default=10.0)


class Comment(models.Model):
	problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
	user = models.ForeignKey(User, default=1, null=True)
	content = models.TextField(max_length=5000)
	pub_date = models.DateTimeField('date published')

	def __str__(self):
		return self.content
