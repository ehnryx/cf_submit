#!/usr/bin/env python

import sys
import os
import argparse
import re
from robobrowser import RoboBrowser
import subprocess
import cf_login
import cf_submit
import cf_standings

""" login """
def login(handle, password):
	browser = RoboBrowser(parser = "lxml")
	browser.open("http://codeforces.com/enter")
	enter_form = browser.get_form("enterForm")
	enter_form["handle"] = handle
	enter_form["password"] = password
	browser.submit_form(enter_form)

	checks = list(map(lambda x: x.getText()[1:].strip(), browser.select("div.caption.titled")))
	if handle not in checks:
		print("Login Corrupted.")
		return None
	else:
		return browser

""" submit problem """
def submit(handle, password, contest, problem, lang, source, watch):
	print("Submitting to problem " + contest + problem.upper() + " as " + handle)

	browser = login(handle, password)

	#browser = RoboBrowser(parser = "lxml")
	if len(contest) >= 6:
		browser.open("http://codeforces.com/gym/" + contest + "/submit/" + problem.upper())
	else:
		browser.open("http://codeforces.com/contest/" + contest + "/submit/" + problem.upper())
	submission = browser.get_form(class_="submit-form")
	if submission is None:
		print("Cannot find problem")
		return
	submission["sourceFile"] = source
	langcode = None
	if lang == "cpp":
		# GNU G++14 6.2.0
		langcode = "50"
		# GNU G++11 5.1.0
		# langcode = "42"
	elif lang == "c":
		# GNU GCC C11 5.1.0
		langcode = "43"
	elif lang == "py":
		# python 2.7.12
		langcode = "7"
		# python 3.5.2
		# langcode = "31"
	elif lang == "java": 
		# Java 1.8.0_112
		langcode = "36"
	else: 
		print("Unknown Language")
		return
	submission["programTypeId"] = langcode

	browser.submit_form(submission)
	
	if browser.url[-3:] != "/my":
		print("Failed to submit code")
		return

	""" show submission """
	print("Code submitted properly")
	if watch:
		cf_submit.watch(handle)

""" print standings """
def print_standings(handle, password, contest, verbose):
	# requires login
	browser = login(handle, password)
	if len(str(contest)) >= 6:
		""" gym contest """
		browser.open("http://codeforces.com/gym/"+contest+"/standings/friends/true")
		raw_html = browser.parsed
	else:
		""" codeforces round """
		browser.open("http://codeforces.com/contest/"+contest+"/standings/friends/true")
		raw_html = browser.parsed
	cf_standings.print_st(raw_html, verbose)


""" main """
def main():
	""" get default gym contest """ 
	defaultcontest = None
	if os.path.isfile("/home/d/d0b1b/Tools/cf_submit/contestid"):
		contestfile = open("/home/d/d0b1b/Tools/cf_submit/contestid", "r")
		defaultcontest = contestfile.read().rstrip('\n')
		contestfile.close()
	else:
		print("Cannot find default contest")
	
	""" argparse """
	parser = argparse.ArgumentParser(description="Command line tool to submit to codeforces", formatter_class=argparse.RawTextHelpFormatter)
	parser.add_argument("command", help="peek -- look at last submission\n" + "watch -- watch last submission\n" + "con/gym -- change contest or gym id\n" + "login -- save login info\n" + "submit -- submit code to problem\n" + "standings -- show standings of friends in default contest, or specify contest with -p")
	parser.add_argument("option", nargs='?', default=None, help="file to submit")
	parser.add_argument("-p", "--prob", action="store", default=None, help="specify problem, example: -p 845a")
	parser.add_argument("-c", "--contest", action="store", default=None, help="specify contest when getting standings")
	parser.add_argument("-w", "--watch", action="store_true", default=False, help="watch submission status")
	parser.add_argument("-v", "--verbose", action="store_true", default=False, help="show more when looking at standings")
	parser.add_argument("-t", "--top", type=int, nargs='?', const=10, default=None, help="number of top contestants to print")
	args = parser.parse_args()

	if args.command == "gym" or args.command == "con":
		""" set contest """
		contest = args.option
		if contest is None: 
			contest = raw_input("Contest/Gym number: ")
		contestfile = open("/home/d/d0b1b/Tools/cf_submit/contestid", "w")
		contestfile.write(contest)
		contestfile.close()
		if len(contest) >= 6:
			print("Gym set to " + contest)
		else:
			print("Contest set to " + contest)
	
	elif args.command == "login":
		""" set login info """
		if args.option is None:
			cf_login.set_login()
		else:
			cf_login.set_login(args.option)

	elif args.command == "peek": 
		""" look at last submission """
		cf_submit.peek(cf_login.get_secret(False))
	
	elif args.command == "watch": 
		cf_submit.watch(cf_login.get_secret(False))

	elif args.command == "standings":
		""" look at friends standings """
		if args.top is None:
			handle, password = cf_login.get_secret(True)
			if args.contest is None:
				print_standings(handle, password, defaultcontest, args.verbose)
			else:
				print_standings(handle, password, args.contest, args.verbose)
		else:
			if args.contest is None:
				cf_standings.print_top(defaultcontest, args.top)
			else:
				cf_standings.print_top(args.contest, args.top)

	elif args.command == "submit":
		""" get handle and password """
		defaulthandle, defaultpass = cf_login.get_secret(True)

		""" split file name """
		source = args.option
		if source is None:
			source = raw_input("File to submit: ")
		info = source.split('.')

		""" submit problem """
		if args.prob is not None:
			if len(args.prob) == 1:
				""" letter only """
				submit(defaulthandle, defaultpass, defaultcontest, args.prob, info[-1], source, args.watch)
			else:
				"""  parse string """
				splitted = re.split('(\D+)', args.prob)
				if len(splitted) == 3 and len(splitted[1]) == 1 and len(splitted[2]) == 0:
					""" probably a good string """
					submit(defaulthandle, defaultpass, splitted[0], splitted[1], info[-1], source, args.watch)
				else: 
					print("cannot understand the problem specified")
		elif len(info) == 2:
			""" try to parse info[0] """
			if len(info[0]) == 1:
				""" only the letter, use default contest """
				submit(defaulthandle, defaultpass, defaultcontest, info[0], info[1], source, args.watch)
			else: 
				""" contest is included, so parse """
				splitted = re.split('(\D+)', info[0])
				if len(splitted) == 3 and len(splitted[1]) == 1 and len(splitted[2]) == 0:
					""" probably good string ? """
					submit(defaulthandle, defaultpass, splitted[0], splitted[1], info[1], source, args.watch)
				else:
					print("cannot parse filename, specify problem with -p or --prob")
		else:
			print("cannot parse filename, specify problem with -p or --prob")
	else:
		print("UNKNOWN COMMAND")


""" END """ 
if __name__ == "__main__":
	try:
		main()
	except KeyboardInterrupt:
		print("")
		sys.exit(0)
