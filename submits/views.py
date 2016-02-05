from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import Submit
from .executer import execute


def index(request):
	if not request.user.is_authenticated():
		return HttpResponseRedirect('/user/')

	submits_list_total = Submit.objects.filter(user=request.user).order_by('-pub_date')

	paginator = Paginator(submits_list_total, 25)
	page = request.GET.get('page')
	try:
		submits_list = paginator.page(page)
	except PageNotAnInteger:
		submits_list = paginator.page(1)
	except EmptyPage:
		submits_list = paginator.page(paginator.num_pages)

	context = {'submits_list': submits_list}
	return render(request, 'submits/index.html', context)


def detail(request, submit_id):
	if not request.user.is_authenticated():
		return HttpResponseRedirect( '/user/')

	try:
		submit = Submit.objects.get(id=submit_id)
	except Submit.DoesNotExist:
		return HttpResponseRedirect( '/submits/')

	if not (submit.user == request.user or request.user.is_staff):
		return HttpResponse("Brak uprawnień")

	context = {'submit': submit}

	execute()
	return render(request, 'submits/detail.html', context)

