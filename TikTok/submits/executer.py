from .models import Submit
from problems.models import TestProgram, Group, Problem
from user.models import MyUser, Ranking

from subprocess import Popen, PIPE
from re import findall
from threading import Timer

executing = False


def execute():
	if executing:
		return

	try:
		subs = Submit.objects.filter(executed=False)
		if len(subs) == 0:
			return

		global executing
		executing = True

		for p in subs:
			p.is_executing = True
			p.save()
			p.output = ""
			p.comment = ""
			tests = TestProgram.objects.filter(problem=p.problem)

			legit = is_mathematica_code_legit(p.code)
			
			accomplishments = 0
			
			if not legit: 
				p.comment += "Użyto niedozwolonego słowa"
			else:
				for test in tests:
					# uruchom kernel
					mathematica_input = p.code + "\n\n" + test.code
					program = Popen(['wolfram'], stdout=PIPE, stdin=PIPE, stderr=PIPE)
					timer = Timer(test.time, program.terminate)
					timer.start()
					output_data = program.communicate(input=bytes(mathematica_input, 'UTF-8'))[0]

					fast_enough = False
					if timer.is_alive():
						timer.cancel()
						fast_enough = True

					if not fast_enough:
						p.comment += "TEST " + str(test.id) + ": Przekroczono limit czasu"
					else:
						output = output_data.decode("utf-8")
						position = output.rfind("ACC:")
						accomplishment_string = output[position + 4:position + 7]

						p.comment += "TEST " + str(test.id) + ":"
						if accomplishment_string == 'YES':
							accomplishments += 1
							p.comment += "OK\n"
						else:
							p.comment += "BŁĄD\n"

						test_comments = findall("\(COMMENT:(.*?):COMMENT\)", output)
						if len(test_comments) > 0:
							p.comment += "TEST " + str(test.id) + " komentarz: " + test_comments[-1] + "\n"

						p.output += output

			p.accomplishment = (accomplishments == len(tests))

			p.is_executing = False
			p.executed = True
			p.save()

			update_stats(p.user, p.problem)
			
	except:
		global executing
		executing = False

	global executing
	executing = False

	execute()


def update_stats(user, problem):
	# MY_USER STATS
	submits_accomplishments = Submit.objects.filter(accomplishment=True, user=user)
	seen = set()
	seen_add = seen.add
	problems_accomplishments = [x.problem for x in submits_accomplishments if not (x.problem in seen or seen_add(x.problem))]
	my_user = MyUser.objects.get(user=user)
	my_user.accomplishments = len(problems_accomplishments)

	my_user.save()

	# PROBLEM STATS
	submits_accomplishments = Submit.objects.filter(problem=problem, accomplishment=True)
	seen = set()
	seen_add = seen.add
	users_accomplishments = [x.user for x in submits_accomplishments if not (x.user in seen or seen_add(x.user))]
	submits_total = Submit.objects.filter(problem=problem)
	seen2 = set()
	seen2_add = seen2.add
	users_total = [x.user for x in submits_total if not (x.user in seen2 or seen2_add(x.user))]

	problem.users_did = len(users_accomplishments)
	problem.users_total = len(users_total)
	problem.save()
	
	# GROUP STATS
	submits_accomplishments = Submit.objects.filter(accomplishment=True, user=user)
	seen = set()
	seen_add = seen.add
	problems_accomplishments = [x.problem for x in submits_accomplishments if x.problem.group == problem.group and not (x.problem in seen or seen_add(x.problem))]
	
	my_user = MyUser.objects.get(user=user)
	try:
		ranking = Ranking.objects.get(my_user=my_user, group=problem.group)
		ranking.did = len(problems_accomplishments)
		ranking.save()
	except Ranking.DoesNotExist:
		if len(problems_accomplishments) > 0:
			ranking = Ranking(my_user=my_user, group=problem.group, did=0)
			ranking.did = len(problems_accomplishments)
			ranking.save()


def is_mathematica_code_legit(code):
	keywords = ['kupa', 'pupa']
	for word in keywords:
		if word in code:
			return False
	return True
