from django.db import models
from django.contrib.auth.models import User


class Group(models.Model):
	name = models.CharField(default='', max_length=255)
	shortname = models.CharField(default='', max_length=255, primary_key=True)
	pub_date = models.DateTimeField('date published')
	problems = models.IntegerField(default=0)
	open = models.BooleanField(default=True)
	
	def __str__(self):
		return self.shortname

		
class Privilege(models.Model):
	group = models.ForeignKey(Group, on_delete=models.CASCADE)
	user = models.ForeignKey(User, default=1, null=True)
	hash = models.CharField(default='', max_length=255)
	used = models.BooleanField(default=False)
	sent = models.CharField(default='', max_length=255)
	
	
class Problem(models.Model):
	group = models.ForeignKey(Group, on_delete=models.CASCADE)
	name = models.CharField(default='', max_length=255)
	user = models.ForeignKey(User, default=1, null=True)
	pdf_file_link = models.CharField(default='', max_length=255)
	pub_date = models.DateTimeField('date published')
	users_total = models.IntegerField(default=0)
	users_did = models.IntegerField(default=0)

	def __str__(self):
		return self.group.shortname+": "+self.name

	def delete(self, *args, **kwargs):
		from submits.models import Submit
		from user.models import MyUser, Ranking

		group = self.group

		shortname = group.shortname
		# update group info
		group.problems = len(Problem.objects.filter(group=group))-1
		group.save()

		# update user info
		submits_accomplishments = Submit.objects.filter(accomplishment=True, problem=self)
		seen = set()
		seen_add = seen.add
		user_accomplishment = [x.user for x in submits_accomplishments if not (x.user in seen or seen_add(x.user))]

		for user in user_accomplishment:
			my_user = MyUser.objects.get(user=user)
			my_user.accomplishments -= 10
			my_user.save()

			try:
				ranking = Ranking.objects.get(my_user=my_user, group=group)
				ranking.did -= 1
				ranking.save()

				if ranking.did == 0:
					ranking.delete()
			except Ranking.DoesNotExist:
				pass

		super(Problem, self).delete(*args, **kwargs)


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
