from django.contrib import admin
from .models import Group, Problem, Comment, TestProgram, Privilege


class GroupAdmin(admin.ModelAdmin):
	list_display = ('name', 'shortname', 'open')
	list_filter = ['name','shortname', 'pub_date', 'open']
	search_fields = ['name']
admin.site.register(Group, GroupAdmin)


class PrivilegeAdmin(admin.ModelAdmin):
	list_display = ('group', 'user', 'hash', 'sent')
admin.site.register(Privilege, PrivilegeAdmin)

class ProblemAdmin(admin.ModelAdmin):
	list_display = ( 'name', 'group', 'user', 'pub_date', 'users_total', 'users_did')
	list_filter = ['group','user', 'pub_date']
	search_fields = ['name']
admin.site.register(Problem, ProblemAdmin)


class CommentAdmin(admin.ModelAdmin):
	list_display = ('content', 'problem', 'user', 'pub_date')
	list_filter = ['user', 'pub_date']
	search_fields = ['content']
admin.site.register(Comment, CommentAdmin)


class TestProgramAdmin(admin.ModelAdmin):
	list_display = ('id', 'problem', 'time')
	list_filter = ['problem']
	search_fields = ['code']
admin.site.register(TestProgram, TestProgramAdmin)
