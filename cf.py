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
import cf_problems
import colours

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
	if len(contest) >= 6:
		browser.open("http://codeforces.com/gym/" + contest + "/submit/" + problem.upper())
	else:
		browser.open("http://codeforces.com/contest/" + contest + "/submit/" + problem.upper())

	""" show submission """
	if cf_submit.submit_problem(browser, contest, lang, source) and watch:
		cf_submit.watch(handle)

""" print standings """
def print_standings(handle, password, contest, verbose, top, sort, showall):
	# requires login
	browser = login(handle, password)
	if len(str(contest)) >= 6:
		""" gym contest """
		url = "http://codeforces.com/gym/"+contest+"/standings"
	else:
		""" codeforces round """
		url = "http://codeforces.com/contest/"+contest+"/standings"
	""" check if friends """ 
	if showall is False:
		url += "/friends/true"
		friends = True
	else:
		url += "/page/1"
		friends = False
	browser.open(url)
	cf_standings.print_st(browser.parsed, verbose, top, sort, friends)

""" print problem stats """
def print_problems(handle, password, contest, verbose, sort):
	browser = login(handle, password)
	if len(str(contest)) >= 6:
		url = "http://codeforces.com/gym/"+contest
	else:
		url = "http://codeforces.com/contest/"+contest
	browser.open(url);
	if sort is None:
		sort = "solves"
	if sort == "solves" or sort == "index":
		cf_problems.print_prob(browser.parsed, contest, verbose, sort)
	else:
		print("UNKNOWN SORT")

""" get time """
def print_time(handle, password, contest):
	browser = login(handle, password)
	if len(str(contest)) >= 6:
		url = "http://codeforces.com/gym/"+contest+"/submit"
	else:
		url = "http://codeforces.com/contest/"+contest+"/submit"
	browser.open(url)
	countdown_timer = browser.parsed.find_all("span", class_="contest-state-regular countdown before-contest-"+contest+"-finish")
	if len(countdown_timer) == 0:
		print("Contest " + contest + " is over")
	else:
		print(colours.bold() + "TIME LEFT: " + str(countdown_timer[0].get_text(strip=True)) + colours.reset())


""" main """
def main():
	""" get default gym contest """ 
	defaultcontest = None
	if os.path.isfile("/home/d/d0b1b/Tools/cf_submit/contestid"):
		contestfile = open("/home/d/d0b1b/Tools/cf_submit/contestid", "r")
		defaultcontest = contestfile.read().rstrip('\n')
		contestfile.close()
	
	""" argparse """
	parser = argparse.ArgumentParser(description="Command line tool to submit to codeforces", formatter_class=argparse.RawTextHelpFormatter)
	parser.add_argument("command", help=
			"con/gym -- change contest or gym id\n" + 
			"info -- current handle and contest id\n" + 
			"login -- save login info\n" + 
			"submit -- submit code to problem\n" + 
			"peek -- look at last submission\n"	+ 
			"watch -- watch last submission\n" + 
			"standings -- show standings of friends in default contest, or specify contest with -p\n" +
			"problems -- show number of solves on each problem\n"
			"time -- shows time left in contest\n"
			)
	parser.add_argument("option", nargs='?', default=None, help="file to submit")
	parser.add_argument("-p", "--prob", action="store", default=None, help="specify problem, example: -p 845a")
	parser.add_argument("-l", "--lang", action="store", default=None, help="specify language, example: -l cpp11")
	parser.add_argument("-c", "--contest", action="store", default=None, help="specify contest when getting standings")
	parser.add_argument("-w", "--watch", action="store_true", default=False, help="watch submission status")
	parser.add_argument("-v", "--verbose", action="store_true", default=False, help="show more when looking at standings")
	parser.add_argument("-a", "--all", action="store_true", default=False, help="show common standings")
	parser.add_argument("-t", "--top", type=int, nargs='?', const=10, default=24, help="number of top contestants to print")
	parser.add_argument("-s", "--sort", type=str, nargs='?', const="solves", default=None, help="sort by: solves (default), index (id)")
	args = parser.parse_args()

	""" deal with short commands """
	if args.command == "st":
		args.command = "standings"
	elif args.command == "pb":
		args.command = "problems"
	if args.sort == "id":
		args.sort = "index"

	""" do stuff """
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
	
	elif args.command == "info": 
		handle = cf_login.get_secret(False)
		print("handle: " + handle)
		print("contestID: " + str(defaultcontest))
	
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

	elif args.command == "time": 
		handle, password = cf_login.get_secret(True)
		if args.contest is None:
			print_time(handle, password, defaultcontest)
		else:
			print_time(handle, password, args.contest)

	elif args.command == "standings":
		""" look at standings """
		handle, password = cf_login.get_secret(True)
		if args.contest is None:
			print_standings(handle, password, defaultcontest, args.verbose, args.top, args.sort, args.all)
		else:
			print_standings(handle, password, args.contest, args.verbose, args.top, args.sort, args.all)

	elif args.command == "problems":
		""" look at problem stats """
		handle, password = cf_login.get_secret(True)
		if args.contest is None: 
			print_problems(handle, password, defaultcontest, args.verbose, args.sort)
		else:
			print_problems(handle, password, args.contest, args.verbose, args.sort)

	elif args.command == "submit":
		""" get handle and password """
		defaulthandle, defaultpass = cf_login.get_secret(True)

		""" split file name """
		source = args.option
		if source is None:
			source = raw_input("File to submit: ")
		info = source.split('.')
		
		""" check language """
		if args.lang is not None:
			info[-1] = args.lang

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
			if info[0][:2].lower() == "cf":
				""" remove the cf """
				info[0] = info[0][2:]
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
