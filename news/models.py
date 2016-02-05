from django.db import models
from django.contrib.auth.models import User


class News(models.Model):
	content = models.TextField(default='')
	user = models.ForeignKey(User, default=1, null=True)
	pub_date = models.DateTimeField('date published')

	def __str__(self):
		return "News " + str(self.id) + ": " + str(self.content[:50])
