from django.contrib import admin

from .models import Submit


class SubmitAdmin(admin.ModelAdmin):
	# fields = [ 'user']
	list_display = ('problem', 'user', 'pub_date', 'is_executing', 'executed', 'accomplishment')
	list_filter = ['problem', 'user', 'pub_date', 'is_executing', 'executed', 'accomplishment']
	search_fields = ['code', 'output', 'comment']

admin.site.register(Submit, SubmitAdmin)
