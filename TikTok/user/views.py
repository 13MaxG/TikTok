from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

from django.contrib.auth import authenticate
from django.contrib.auth import login as django_login
from django.contrib.auth import logout as django_logout
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


from .forms import LoginForm, RegisterForm, EditForm, EditPasswordForm

from .models import MyUser, Ranking
from submits.models import Submit
from problems.models import Group, Privilege


def index(request):
	if request.user.is_authenticated():
		message = 'zalogowany jako ' + request.user.username
	else:
		message = 'nie zalogowany'
	context = {'message': message}
	return render(request, 'user/index.html', context)


def login(request):
	form = LoginForm()
	message = ''
	if request.method == 'POST':
		form = LoginForm(request.POST)
		if form.is_valid():
			username = form.cleaned_data['login']
			password = form.cleaned_data['password']
			user = authenticate(username=username, password=password)
			if user is not None:
				django_login(request, user)
				return HttpResponseRedirect('/')
			else:
				message = 'Nie udało się zalogować'

	return render(request, 'user/login.html', {'form': form, 'message': message})


def logout(request):
	django_logout(request)
	return HttpResponseRedirect('/')


def register(request):
	if request.user.is_authenticated():
		return HttpResponseRedirect('/')

	form = RegisterForm()
	message = ''
	if request.method == 'POST':
		form = RegisterForm(request.POST)
		if form.is_valid():
			username = form.cleaned_data['login']
			email = form.cleaned_data['email'].lower()
			password = form.cleaned_data['password']
			password2 = form.cleaned_data['password2']
			first_name = form.cleaned_data['first_name']
			last_name = form.cleaned_data['last_name']
			motto = form.cleaned_data['motto']

			if password != password2:
				message = 'Hasła się nie zgadzają'
			else:
				if len(User.objects.filter(email=email)) != 0:
					message = 'Taki email jest już zajęty. '
				else:
					if len(User.objects.filter(username=username)) != 0:
						message = 'Taki login jest już zajęty'
					else:
						user = User.objects.create_user(username, email, password)
						user.first_name = first_name
						user.last_name = last_name
						user.save()
						my_user = MyUser(user=user, motto=motto)
						my_user.save()
						user = authenticate(username=username, password=password)
						django_login(request, user)

						return HttpResponseRedirect('/')

	return render(request, 'user/register.html', {'form': form, 'message': message})


def detail(request, user_id):
	try:
		user = User.objects.get(id=user_id)
	except User.DoesNotExist:
		return HttpResponse("Błąd")

	my_user = MyUser.objects.get(user=user)

	
	submits_accomplishments = Submit.objects.filter(accomplishment=True, user=user)
	seen = set()
	seen_add = seen.add
	problems_accomplishments = [x.problem for x in submits_accomplishments if not (x.problem in seen or seen_add(x.problem))]

	submits_total = Submit.objects.filter(user=user)
	seen2 = set()
	seen2_add = seen2.add
	problems_tried = [x.problem for x in submits_total if not (x.problem in problems_accomplishments or x.problem in seen2 or seen2_add(x.problem))]

	context = {'c_user': user, 'my_user': my_user, 'problems_accomplishments': problems_accomplishments, 'problems_tried': problems_tried}
	return render(request, 'user/detail.html', context)


def edit(request):
	if not request.user.is_authenticated():
		return HttpResponseRedirect('/user/')

	message = ''
	user = request.user
	my_user = MyUser.objects.get(user=user)

	if request.method == 'POST':
		form = EditForm(request.POST)
		if form.is_valid():
			email = form.cleaned_data['email'].lower()
			
			email_ok = True
			try:
				x = User.objects.filter(email=email)
				if x != user:
					email_ok = False
			except User.DoesNotExist:
				pass
				
			if email_ok:
					message = 'Taki email jest już zajęty. '
			else:
				user.email = form.cleaned_data['email'].lower()
				user.first_name = form.cleaned_data['first_name']
				user.last_name = form.cleaned_data['last_name']
				my_user.motto = form.cleaned_data['motto']

				user.save()
				my_user.save()
				return HttpResponseRedirect('/user/%s/detail' %user.id)
		else:
			message = "Podaj hasło"
	else:
		form = EditForm({'email': user.email, 'login': user.username, 'first_name': user.first_name, 'last_name': user.last_name, 'motto': my_user.motto})
		form.fields['login'].widget.attrs['readonly'] = True

	return render(request, 'user/edit.html', {'form': form, 'message': message})


def edit_password(request):
	if not request.user.is_authenticated():
		return HttpResponseRedirect('/user/')
	form = EditPasswordForm()
	message=''
	if request.method == 'POST':
		form = EditPasswordForm(request.POST)
		if form.is_valid():
			pass0 = form.cleaned_data['password0']
			pass1 = form.cleaned_data['password1']
			pass2 = form.cleaned_data['password2']

			prev_user = request.user
			username = request.user.username

			user2 = authenticate(username=request.user.username,password=pass0)
			if user2 is None:
				message = "Niewłaściwe stare hasło!"
			else:
				django_login(request, user2)

				if username == request.user.username:
					if pass1 != '' and pass1 == pass2:
						request.user.set_password(pass1)
						request.user.save()

						user = authenticate(username=username, password=pass1)
						django_login(request, user)
						return HttpResponseRedirect('/user/%s/detail'%request.user.id)
					else:
						message = "Hasła się nie zgadzają"
		else:
			message = "błąd formularza"
	return render(request, 'user/edit_password.html', {'form': form, 'message': message})


def ranking(request, shortname):
	
	try:	
		group = Group.objects.get(shortname=shortname)
	except Group.DoesNotExist:
		return HttpResponseRedirect('/problems/groups/')
	
	tmp = check_user_priviledge(request, group)
	if tmp != True:
		return tmp

	request.session['group'] = shortname

	list_total = Ranking.objects.filter(group=group).order_by('-did')
	
	paginator = Paginator(list_total, 25)
	page = request.GET.get('page')
	try:
		my_list = paginator.page(page)
	except PageNotAnInteger:
		my_list = paginator.page(1)
	except EmptyPage:
		my_list = paginator.page(paginator.num_pages)

	return render(request, 'user/ranking.html', {'my_list': my_list, 'group': group})

	
def check_user(request):
	if not request.user.is_authenticated():
		return HttpResponseRedirect('/user/')
	return True

		
def check_admin(request):
	if not request.user.is_staff:
		return HttpResponse("Brak uprawnień")
	return True
		
def check_user_priviledge(request, group):
	tmp = check_user(request)
	if tmp != True:
		return tmp
		
	if not group.open and not request.user.is_staff:
		try:
			privilege = Privilege.objects.get(user=request.user, group=group)
		except Privilege.DoesNotExist:
			return HttpResponseRedirect('/problems/groups/'+group.shortname+'/get_privilege')
	return True