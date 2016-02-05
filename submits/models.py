from django.db import models
from django.contrib.auth.models import User

from problems.models import Problem


class Submit(models.Model):
	problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
	user = models.ForeignKey(User, default=1, null=True)
	pub_date = models.DateTimeField('date published')
	code = models.TextField(max_length=100000)
	output = models.TextField(default="")
	accomplishment = models.BooleanField(default=False)
	executed = models.BooleanField(default=False)
	is_executing = models.BooleanField(default=False)
	comment = models.TextField(default="")

	def __str__(self):
		return "Submit nr " + str(self.id) + "do zadania" + str(self.problem)
