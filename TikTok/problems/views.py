from threading import Thread
from os import path, makedirs
from re import compile
from uuid import uuid4
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.utils import timezone
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from submits.executer import execute
from submits.models import Submit
from user.models import MyUser, Ranking
from user.views import check_user,check_admin,check_user_priviledge
from .forms import CommentForm, SubmitForm, CreateForm, TestProgramForm, DeletionForm, EditNameForm, EditPDFForm, CreateGroupForm, GetPrivilegeForm
from .models import Group, Problem, Comment, TestProgram, Privilege


def index(request, shortname):
	# shortname = "MAIN";
	# if request.session['group'] != "":
	# shortname = request.session['group']
	try:	
		group = Group.objects.get(shortname=shortname)
	except Group.DoesNotExist:
		return HttpResponseRedirect('/problems/groups/')
		
	request.session['group']  = shortname
	
	if not group.open:
		tmp = check_user_priviledge(request, group)
		if tmp != True:
			return tmp
	
	problems_list_total = Problem.objects.filter(group=group).order_by('pub_date')

	paginator = Paginator(problems_list_total, 25)
	page = request.GET.get('page')
	try:
		problems_list = paginator.page(page)
	except PageNotAnInteger:
		problems_list = paginator.page(1)
	except EmptyPage:
		problems_list = paginator.page(paginator.num_pages)

	return render(request, 'problems/index.html', {'problems_list': problems_list, 'group': group})

def get_privilege(request, shortname):
	try:	
		group = Group.objects.get(shortname=shortname)
	except Group.DoesNotExist:
		return HttpResponseRedirect('/problems/groups/')
		
	if group.open:
		return HttpResponse("Konkurs jest dostępny")
		
	request.session['group']  = shortname
	
	tmp = check_user(request)
	if tmp != True:
		return tmp
		
	
	form = GetPrivilegeForm()
	message=''
	if request.method == 'POST':
		form = GetPrivilegeForm(request.POST)
		if form.is_valid():
			hash = form.cleaned_data['hash']
			if hash != '---':
				try:
					privilege = Privilege.objects.get(group=group, hash=hash)
					privilege.user = request.user
					privilege.hash = '---'
					privilege.save()
					return HttpResponseRedirect('/problems/list/%s/' % group.shortname)
				except Privilege.DoesNotExist:
					message = 'Niepoprawny kod dostępu'

		else:
			form = GetPrivilegeForm()
			message = "Błąd w formularzu"
			
			
	return render(request, 'problems/get_privilege.html', {'message': message, 'group': group, 'form': form})
	
def groups(request):
	main = Group.objects.all()[0]
	
	group_list_total = list(Group.objects.all().order_by('-pub_date'))
	group_list_total.remove(main)
	paginator = Paginator(group_list_total, 25)
	page = request.GET.get('page')
	try:
		groups_list = paginator.page(page)
	except PageNotAnInteger:
		groups_list = paginator.page(1)
	except EmptyPage:
		groups_list = paginator.page(paginator.num_pages)

	return render(request, 'problems/groups.html', {'groups_list': groups_list, 'main': main})


def set_active_group(request, group_shortname):
	request.session['group'] = group_shortname
	return HttpResponseRedirect('/problems/list/'+group_shortname+'/')

	
def detail(request, problem_id):
	try:
		problem = Problem.objects.get(id=problem_id)
	except Problem.DoesNotExist:
		return HttpResponse("Nie istnieje taki problem")

	group = Group.objects.get(problem=problem)
	request.session['group'] = group.shortname
	
	tmp = check_user_priviledge(request, group)
	if tmp != True:
		return tmp

	tests = TestProgram.objects.filter(problem=problem)
	list_of_comments = Comment.objects.filter(problem=problem)
	context = {'problem': problem, 'tests': tests, 'comments_num': len(list_of_comments)}
	return render(request, 'problems/detail.html', context)

	
def comments(request, problem_id):
	try:
		problem = Problem.objects.get(id=problem_id)
	except Problem.DoesNotExist:
		return HttpResponse("Nie istnieje taki problem")

	tmp = check_user_priviledge(request, problem.group)
	if tmp != True:
		return tmp
		
	comments_list_total = Comment.objects.filter(problem=problem)
	form = CommentForm()

	paginator = Paginator(comments_list_total, 10)
	page = request.GET.get('page')
	try:
		comment_list = paginator.page(page)
	except PageNotAnInteger:
		comment_list = paginator.page(1)
	except EmptyPage:
		comment_list = paginator.page(paginator.num_pages)

	context = {'problem': problem, 'comment_list': comment_list, 'form': form}
	return render(request, 'problems/comments.html', context)


def comment(request, problem_id):
	
	message = ''
	form = CommentForm()
	problem = Problem.objects.get(id=problem_id)
	
	tmp = check_user_priviledge(request, problem.group)
	if tmp != True:
		return tmp
		
	if request.method == 'POST':
		form = CommentForm(request.POST)
		if form.is_valid():
			if len(form.cleaned_data['content']) > 5000:
				return HttpResponse("Za długi komentarz")
			problem.comment_set.create(content=form.cleaned_data['content'], pub_date=timezone.now(), user=request.user)

			return HttpResponseRedirect('/problems/%s/comments' % problem_id)
		else:
			form = CommentForm()
			message = "Błąd w formularzu"

	return render(request, 'problems/comment.html', {'problem': problem, 'form': form, 'message': message})


def submit(request, problem_id):
	if not request.user.is_authenticated():
		return HttpResponseRedirect('/user/')

	form = SubmitForm()
	problem = Problem.objects.get(id=problem_id)
	
	tmp = check_user_priviledge(request, problem.group)
	if tmp != True:
		return tmp
		
		
	if request.method == 'POST':
		form = SubmitForm(request.POST)
		if form.is_valid():
			if len(form.cleaned_data['code']) > 100000:
				return HttpResponse("Za długi program")
			problem.submit_set.create(code=form.cleaned_data['code'], pub_date=timezone.now(), user=request.user)

			thr = Thread(target=execute)
			thr.start()
			# execute()
			return HttpResponseRedirect('/submits')
		else:
			form = SubmitForm()
	return render(request, 'problems/submit.html', {'problem': problem, 'form': form})


def download(request, problem_id):
	try:
		problem = Problem.objects.get(id=problem_id)
		
		tmp = check_user_priviledge(request, problem.group)
		if tmp != True:
			return tmp
		
		file = open(problem.pdf_file_link, 'rb')
		response = HttpResponse(file, content_type='application/pdf')
		return response
	except Problem.DoesNotExist:
		return HttpResponse(request, "Nie istnieje taki problem")


def edit_group(request, shortname):				
	try:
		group = Group.objects.get(shortname=shortname)
	except Group.DoesNotExist:
		return HttpResponse("Nie istnieje taki konkurs")
	
	tmp = check_admin(request)
	if tmp != True:
		return tmp	
	
	message = ''
	form =  CreateGroupForm({'name': group.name, 'shortname': group.shortname, 'open':group.open})
	
	if request.method == 'POST':
		form = CreateGroupForm(request.POST)
		if form.is_valid():
			pattern = compile('^[a-zA-Z0-9]+$')
			if not pattern.match(form.cleaned_data['shortname']):
				return HttpResponse("Niewłaściwa nazwa skrótu konkursu.")
				
			group.name = form.cleaned_data['name']
			
			if group.shortname == 'MAIN' and (form.cleaned_data['shortname'] != group.shortname or (form.cleaned_data['name']=="True") != group.open):
				return HttpResponse("Nie można zmienić skrótu konkursu MAIN lub jego dostępności")
				
			group.shortname = form.cleaned_data['shortname']
			group.open = (form.cleaned_data['name']=="True")
			
			group.save()
			request.session['group'] = group.shortname
			return HttpResponseRedirect('/problems/list/' + group.shortname)
		else:
			form = CreateGroupForm()
			message = "chyba coś się stało źle"
	context = {'form': form, 'message': message, 'group': group}
	return render(request, 'problems/edit_group.html', context)
		

def create_group(request):
	tmp = check_admin(request)
	if tmp != True:
		return tmp

	message = ''
	form = CreateGroupForm()
	if request.method == 'POST':
		form = CreateGroupForm(request.POST)
		if form.is_valid():
			pattern = compile('^[a-zA-Z0-9]+$')
			if not pattern.match(form.cleaned_data['shortname']):
				return HttpResponse("Niewłaściwa nazwa skrótu konkursu.")
				
			try:
				collision  = Group.objects.get(shortname=form.cleaned_data['shortname'])
				return HttpResponse("Nie można utworzyć dwóch konkursów o takim samym skrócie")
			except Group.DoesNotExist:
				group = Group(name=form.cleaned_data['name'], shortname=form.cleaned_data['shortname'], pub_date=timezone.now())
				group.open = (form.cleaned_data['name']=="True")
				
				group.save()
				request.session['group'] = group.shortname
				return HttpResponseRedirect('/problems/list/' + group.shortname)
		else:
			form = CreateGroupForm()
			message = "chyba coś się stało źle"
	context = {'form': form, 'message': message}
	return render(request, 'problems/create_group.html', context)

	
def create(request):
	tmp = check_admin(request)
	if tmp != True:
		return tmp
		
	shortname = "MAIN"
	if request.session['group'] != "":
		shortname = request.session['group']

	try:	
		group = Group.objects.get(shortname=shortname)
	except Group.DoesNotExist:
		return HttpResponseRedirect('/problems/groups/')
		
	message = ''
	form = CreateForm()
	if request.method == 'POST':
		form = CreateForm(request.POST, request.FILES)
		if form.is_valid():
			try:
				last = Problem.objects.latest('id')
			except Problem.DoesNotExist:
				last = None

			next_id = 1
			if last is not None:
				next_id = last.id + 1

			my_file = request.FILES['pdf_file']
			
			if my_file.content_type != 'application/pdf':
				return HttpResponse("Niedozwolony format pliku. Tylko PDF.")
				
			if my_file.size > 20971520: # 20 MB
				return HttpResponse("Maksymalny rozmiar to 20MB.")
			
			if not path.exists('problems/pdf'):
				makedirs('problems/pdf')
			
			filename = 'problems/pdf/problem' + str(next_id) + '.pdf'
			with open(filename, 'wb+') as destination:
				for chunk in my_file.chunks():
					destination.write(chunk)

			prob = Problem(group=group, name=form.cleaned_data['name'], user=request.user, pub_date=timezone.now(), pdf_file_link=filename)
			prob.save()
			group.problems = len(Problem.objects.filter(group=group))
			group.save()
			return HttpResponseRedirect('/problems/list/'+group.shortname)
		else:
			form = CreateForm()
			message = "chyba coś się stało źle"
	context = {'form': form, 'message': message, 'group': group}
	return render(request, 'problems/create.html', context)


def add_test(request, problem_id):
	tmp = check_admin(request)
	if tmp != True:
		return tmp	

	try:
		problem = Problem.objects.get(id=problem_id)
	except TestProgram.DoesNotExist:
		return HttpResponse("Nie istnieje taki problem")

	form = TestProgramForm()

	if request.method == 'POST':
		form = TestProgramForm(request.POST)
		if form.is_valid():
			t = TestProgram(problem=problem, code=form.cleaned_data['code'], time=form.cleaned_data['time'])

			t.save()
			return HttpResponseRedirect('/problems/%s' % problem_id)
		else:
			form = TestProgramForm()
	return render(request, 'problems/add_test.html', {'problem': problem, 'form': form})

def privileges(request, shortname):		
	tmp = check_admin(request)
	if tmp != True:
		return tmp		
		
	try:
		group = Group.objects.get(shortname=shortname)
	except Group.DoesNotExist:
		return HttpResponse("Nie istnieje taki konkurs")
		
	message = ''
	privileges_list = Privilege.objects.filter(group=group, sent=False).exclude(hash='---')

	if request.method == 'POST':
		privilege = Privilege(group = group, hash = uuid4().hex)
		message="przywilej to: " + privilege.hash
		privilege.save()

	context = {'message': message, 'group': group, 'privileges_list': privileges_list}
	return render(request, 'problems/privileges.html', context)
		
		
def edit_test(request, test_id):
	tmp = check_admin(request)
	if tmp != True:
		return tmp		

	try:
		test_program = TestProgram.objects.get(id=test_id)
	except TestProgram.DoesNotExist:
		return HttpResponse("Nie istnieje taki test")

	form = TestProgramForm({'code': test_program.code, 'time': test_program.time})

	if request.method == 'POST':
		form = TestProgramForm(request.POST)
		if form.is_valid():
			test_program.code = form.cleaned_data['code']
			test_program.time = form.cleaned_data['time']

			test_program.save()
			return HttpResponseRedirect('/problems/%s' % test_program.problem.id)
	return render(request, 'problems/edit_test.html', {'test': test_program, 'form': form})


def delete_test(request, test_id):
	tmp = check_admin(request)
	if tmp != True:
		return tmp		
		
	try:
		test_program = TestProgram.objects.get(id=test_id)
		problem = test_program.problem

		test_program.delete()
		return HttpResponseRedirect('/problems/%s' % problem.id)
	except TestProgram.DoesNotExist:
		return HttpResponse("Nie istnieje taki problem")


def delete_problem(request, problem_id):
	tmp = check_admin(request)
	if tmp != True:
		return tmp		
		
	try:
		problem = Problem.objects.get(id=problem_id)
	except TestProgram.DoesNotExist:
		return HttpResponse("Nie istnieje taki problem")

	if request.method == 'POST':
		form = DeletionForm(request.POST)
		if form.is_valid():
			if form.cleaned_data['name'] == problem.name:
				shortname = problem.group.shortname
				problem.delete()
				
				return HttpResponseRedirect('/problems/list/'+shortname)
			else:
				return HttpResponse("Błąd potwierdzenia")
		else:
			return HttpResponse("Błąd potwierdzenia")
	else:
		form = DeletionForm()
	return render(request, 'problems/delete_problem.html', {'problem': problem, 'form': form})

	
def delete_group(request, shortname):
	tmp = check_admin(request)
	if tmp != True:
		return tmp		
		
	try:
		group = Group.objects.get(shortname=shortname)
	except Group.DoesNotExist:
		return HttpResponse("Nie istnieje taki konkurs")

	if shortname == 'MAIN':
		return HttpResponse("Nie można usunąć głównego konkursu")
	if request.method == 'POST':
		form = DeletionForm(request.POST)
		if form.is_valid():
			if form.cleaned_data['name'] == group.name:
				group.delete()
				request.session['group'] = 'MAIN'
				return HttpResponseRedirect('/problems/groups/')
			else:
				return HttpResponse("Błąd potwierdzenia")
		else:
			return HttpResponse("Błąd potwierdzenia")
	else:
		form = DeletionForm()
	return render(request, 'problems/delete_group.html', {'group': group, 'form': form})


def edit_name(request, problem_id):
	tmp = check_admin(request)
	if tmp != True:
		return tmp	
		
	try:
		problem = Problem.objects.get(id=problem_id)
	except TestProgram.DoesNotExist:
		return HttpResponse("Nie istnieje taki problem")

	message = ''
	form = EditNameForm({'name': problem.name})

	if request.method == 'POST':
		form = EditNameForm(request.POST)
		if form.is_valid():
			problem.name = form.cleaned_data['name']
			problem.save()
			return HttpResponseRedirect('/problems/%s' % problem.id)
		else:
			form = EditNameForm()
			message = "chyba coś się stało źle"
	context = {'form': form, 'message': message, 'problem': problem}
	return render(request, 'problems/edit_name.html', context)


def edit_pdf(request, problem_id):
	tmp = check_admin(request)
	if tmp != True:
		return tmp	

	try:
		problem = Problem.objects.get(id=problem_id)
	except TestProgram.DoesNotExist:
		return HttpResponse("Nie istnieje taki problem")

	message = ''
	form = EditPDFForm()
	if request.method == 'POST':
		form = EditPDFForm(request.POST, request.FILES)
		if form.is_valid():

			my_file = request.FILES['pdf_file']
			filename = 'problems/pdf/problem' + str(problem.id) + '.pdf'
			with open(filename, 'wb+') as destination:
				for chunk in my_file.chunks():
					destination.write(chunk)

			problem.pdf_file_link = filename

			problem.save()
			return HttpResponseRedirect('/problems/%s' % problem.id)
		else:
			form = EditPDFForm()
			message = "chyba coś się stało źle"
	context = {'form': form, 'message': message, 'problem': problem}
	return render(request, 'problems/edit_pdf.html', context)


def show_submits(request, problem_id):

	try:
		problem = Problem.objects.get(id=problem_id)
	except TestProgram.DoesNotExist:
		return HttpResponse("Nie istnieje taki problem")

	tmp = check_user_priviledge(request, problem.group)
	if tmp != True:
		return tmp
		
	if request.user.is_staff:
		submits_list_total = Submit.objects.filter(problem=problem).order_by('-pub_date')
	else:
		submits_list_total = Submit.objects.filter(problem=problem, user=request.user).order_by('-pub_date')

	paginator = Paginator(submits_list_total, 25)
	page = request.GET.get('page')
	try:
		submits_list = paginator.page(page)
	except PageNotAnInteger:
		submits_list = paginator.page(1)
	except EmptyPage:
		submits_list = paginator.page(paginator.num_pages)

	return render(request, 'problems/show_submits.html', {'problem': problem, 'submits_list': submits_list})

