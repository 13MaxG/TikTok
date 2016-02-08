from django.contrib import admin
from .models import News


class NewsAdmin(admin.ModelAdmin):
	list_display = ('content', 'user', 'pub_date')
	list_filter = ['user', 'pub_date']
	search_fields = ['content']

admin.site.register(News, NewsAdmin)

