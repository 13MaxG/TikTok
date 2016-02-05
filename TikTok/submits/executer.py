from .models import Submit
from problems.models import TestProgram
from user.models import MyUser

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

			accomplishments = 0
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

			submits_accomplishments = Submit.objects.filter(accomplishment=True, user=p.user)
			seen = set()
			seen_add = seen.add
			problems_accomplishments = [x.problem for x in submits_accomplishments if not (x.problem in seen or seen_add(x.problem))]
			my_user = MyUser.objects.get(user=p.user)
			my_user.accomplishments = len(problems_accomplishments)

			my_user.save()

			# uaktualnij informacje o próbach i sukcesach
			submits_accomplishments = Submit.objects.filter(problem=p.problem, accomplishment=True)
			seen = set()
			seen_add = seen.add
			users_accomplishments = [x.user for x in submits_accomplishments if not (x.user in seen or seen_add(x.user))]
			submits_total = Submit.objects.filter(problem=p.problem)
			seen2 = set()
			seen2_add = seen2.add
			users_total = [x.user for x in submits_total if not (x.user in seen2 or seen2_add(x.user))]

			p.problem.users_did = len(users_accomplishments)
			p.problem.users_total = len(users_total)
			p.problem.save()
	except:
		global executing
		executing = False

	global executing
	executing = False

	execute()
