import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "TikTok.settings")
django.setup()

from problems.models import Group
from user.models import MyUser
from django.utils import timezone
from django.contrib.auth.models import User

if __name__ == '__main__':
	x = Group(name=u'Główny zbiór zadań', shortname="MAIN9", pub_date = timezone.now())
	x.save()

	admin = MyUser(user=User.objects.all()[0])
	admin.save()