import os
import sys
from django.core.wsgi import get_wsgi_application

dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "/../")
sys.path.append(dir)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "TikTok.settings")

application = get_wsgi_application()
