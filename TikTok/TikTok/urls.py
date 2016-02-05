from django.conf.urls import include, url
from django.contrib import admin

from news import views


urlpatterns = [
	url(r'^$', views.main_page, name='main_page'),
	url(r'^news/', include('news.urls')),
	url(r'^user/', include('user.urls')),
	url(r'^problems/', include('problems.urls')),
	url(r'^submits/', include('submits.urls')),
	url(r'^admin/', admin.site.urls),
]
