import os
import sys
from django.core.wsgi import get_wsgi_application

my_dir = os.path.abspath(__file__+"/../../")
sys.path.append(my_dir)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "TikTok.settings")

application = get_wsgi_application()
