from django.contrib import admin

from .models import MyUser, Ranking


class MyUserAdmin(admin.ModelAdmin):
	list_display = ('user', 'motto', 'accomplishments')
	list_filter = ['accomplishments']
	search_fields = ['motto']

admin.site.register(MyUser, MyUserAdmin)


class RankingAdmin(admin.ModelAdmin):
	list_display = ('my_user', 'group', 'did')
	list_filter = ['my_user', 'group', 'did']
	search_fields = ['my_user']
admin.site.register(Ranking, RankingAdmin)