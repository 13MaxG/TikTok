from django.conf.urls import url

from . import views
app_name = 'problems'
urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'^(?P<problem_id>[0-9]+)/$', views.detail, name='detail'),
	url(r'^(?P<problem_id>[0-9]+)/submit$', views.submit, name='submit'),
	url(r'^(?P<problem_id>[0-9]+)/comments$', views.comments, name='comments'),
	url(r'^(?P<problem_id>[0-9]+)/comment$', views.comment, name='comment'),
	url(r'^(?P<problem_id>[0-9]+)/submit$', views.submit, name='submit'),
	url(r'^(?P<problem_id>[0-9]+)/download$', views.download, name='download'),
	url(r'^(?P<problem_id>[0-9]+)/add_test$', views.add_test, name='add_test'),
	url(r'^edit_test/(?P<test_id>[0-9]+)/', views.edit_test, name='edit_test'),
	url(r'^delete_test/(?P<test_id>[0-9]+)/', views.delete_test, name='delete_test'),
	url(r'^(?P<problem_id>[0-9]+)/delete_problem', views.delete_problem, name='delete_problem'),
	url(r'^(?P<problem_id>[0-9]+)/edit_name', views.edit_name, name='edit_name'),
	url(r'^(?P<problem_id>[0-9]+)/edit_pdf', views.edit_pdf, name='edit_pdf'),
	url(r'^(?P<problem_id>[0-9]+)/show_submits', views.show_submits, name='show_submits'),
	url('create', views.create, name='create'),

]
