from django.conf.urls import url

from . import views


app_name = 'user'
urlpatterns = [
	url(r'^$', views.index, name='index'),
	url('login', views.login, name='login'),
	url('logout', views.logout, name='logout'),
	url('register', views.register, name='register'),
	url(r'^(?P<user_id>[0-9]+)/detail', views.detail, name='detail'),
	url(r'edit$', views.edit, name='edit'),
	url(r'edit_password$', views.edit_password, name='edit_password'),
	url(r'ranking', views.ranking, name='ranking'),
]
