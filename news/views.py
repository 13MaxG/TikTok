from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.utils import timezone
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .forms import NewsForm
from .models import News


def main_page(request):
	news_list = News.objects.order_by('-pub_date')[:2]
	context = {'news_list': news_list}
	return render(request, 'news/main_page.html', context)


def index(request):
	news_list_total = News.objects.order_by('-pub_date')

	paginator = Paginator(news_list_total, 5)
	page = request.GET.get('page')
	try:
		news_list = paginator.page(page)
	except PageNotAnInteger:
		news_list = paginator.page(1)
	except EmptyPage:
		news_list = paginator.page(paginator.num_pages)

	return render(request, 'news/index.html', {'news_list': news_list})


def create(request):
	if not request.user.is_authenticated():
		return HttpResponseRedirect('/user/')
	if not request.user.is_staff:
		return HttpResponse("Brak uprawnień")

	message = ''
	form = NewsForm()
	if request.method == 'POST':
		form = NewsForm(request.POST)
		if form.is_valid():
			news = News(content=form.cleaned_data['content'], pub_date=timezone.now(), user=request.user)
			news.save()
			return HttpResponseRedirect('/news/')
		else:
			form = NewsForm()
			message = "Błąd w formularzu"
	
	return render(request, 'news/create.html', {'form': form, 'message': message})
