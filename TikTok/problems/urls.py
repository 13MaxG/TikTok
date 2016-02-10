from django.conf.urls import url

from . import views
app_name = 'problems'
urlpatterns = [
	url(r'^list/(?P<shortname>[0-9a-zA-Z]+)/$', views.index, name='index'),
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
	url(r'^create/', views.create, name='create'),
	url(r'^create_group', views.create_group, name='create_group'),
	url(r'^groups[/]$', views.groups, name='groups'),
	url(r'^set_active_group/(?P<group_shortname>[0-9a-zA-Z]+)', views.set_active_group, name='set_active_group'),
	url(r'^delete_group/(?P<shortname>[0-9a-zA-Z]+)', views.delete_group, name='delete_group'),
	url(r'^edit_group/(?P<shortname>[0-9a-zA-Z]+)', views.edit_group, name='edit_group'),
	url(r'^privileges/(?P<shortname>[0-9a-zA-Z]+)[/]$', views.privileges, name='privileges'),
	url(r'^send_privileges/(?P<shortname>[0-9a-zA-Z]+)', views.send_privileges, name='send_privileges'),
	url(r'^delete_privilege/(?P<shortname>[0-9a-zA-Z]+)/(?P<hash>[0-9a-zA-Z]+)', views.delete_privilege, name='delete_privilege'),
	url(r'^groups/(?P<shortname>[0-9a-zA-Z]+)/get_privilege', views.get_privilege, name='get_privilege'),
]
