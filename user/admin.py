from django.contrib import admin

from .models import MyUser


class MyUserAdmin(admin.ModelAdmin):
	list_display = ('user', 'motto', 'accomplishments')
	list_filter = ['accomplishments']
	search_fields = ['motto']

admin.site.register(MyUser, MyUserAdmin)
