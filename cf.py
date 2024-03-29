#!/usr/bin/env python3

import sys
import os
import argparse
import re
from robobrowser import RoboBrowser
import cf_coach
import cf_login
import cf_problems
import cf_standings
import cf_submit
import cf_test
import colours

""" print standings """
def print_standings(contest, verbose, top, sort, showall):
    # requires login
    browser = cf_login.login()
    if len(str(contest)) >= 6:
        """ gym contest """
        url = "http://codeforces.com/gym/"+contest+"/standings"
    else:
        """ codeforces round """
        url = "http://codeforces.com/contest/"+contest+"/standings"
    """ check if friends """
    if showall is False:
        url += "/friends/true"
    else:
        url += "/page/1"
    browser.open(url)
    cf_standings.print_st(browser.parsed, verbose, top, sort)

""" print problem stats """
def print_problems(contest, verbose, sort):
    browser = cf_login.login()
    if len(str(contest)) >= 6:
        url = "http://codeforces.com/gym/"+contest
    else:
        url = "http://codeforces.com/contest/"+contest
    browser.open(url);
    if sort is None:
        sort = "solves"
    cf_problems.print_prob(browser.parsed, contest, verbose, sort)

""" get time """
def print_time(contest):
    browser = cf_login.login()
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
    contest_loc = os.path.join(os.path.dirname(__file__), "contestid");
    if os.path.isfile(contest_loc):
        contestfile = open(contest_loc, "r")
        defaultcontest = contestfile.read().rstrip('\n')
        contestfile.close()

    """ ------------------- argparse -------------------- """
    parser = argparse.ArgumentParser(description="Command line tool to submit to codeforces", formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("command", help=
            "con/gym -- change contest or gym id\n" +
            "ext -- change default file extension\n" +
            "info -- current handle and contest id\n" +
            "login -- save login info\n" +
            "peek -- look at last submission\n"    +
            "problems -- show number of solves on each problem\n"
            "standings -- show standings of friends in default contest, or specify contest with -p\n" +
            "submit -- submit code to problem\n" +
            "time -- shows time left in contest\n" +
            "test -- tests a problem by running the code on .in and comparing with .ans\n" +
            "watch -- watch last submission\n" +
            "coach -- toggle coach mode\n"
    )
    parser.add_argument("option",
            nargs='*', default=None,
            help="file to submit"
    )
    parser.add_argument("-p", "--prob",
            action="store", default=None,
            help="specify problem, example: -p 845a"
    )
    parser.add_argument("-l", "--lang",
            action="store", default=None,
            help="specify language, example: -l cpp11"
    )
    parser.add_argument("-c", "--contest",
            action="store", default=None,
            help="specify contest when getting standings"
    )
    parser.add_argument("-w", "--watch",
            action="store_true", default=False,
            help="watch submission status"
    )
    parser.add_argument("-v", "--verbose",
            action="store_true", default=False,
            help="show more when looking at standings"
    )
    parser.add_argument("-a", "--all",
            action="store_true", default=False,
            help="show common standings"
    )
    parser.add_argument("-t", "--top",
            type=int, nargs='?', const=10, default=50,
            help="number of top contestants to print"
    )
    parser.add_argument("-s", "--sort",
            choices=["solves", "index", "id"],
            type=str, nargs='?', const="solves", default=None,
            help="sort by: solves (default), index (id)"
    )
    parser.add_argument("-g", "--guru",
            action="store_true", default=False,
            help="submit to acmsguru problemset"
    )
    args = parser.parse_args()

    """ -------------------------------------------------- """
    """ deal with short commands """
    if args.command == "st":
        args.command = "standings"
    elif args.command == "pb":
        args.command = "problems"
    if args.sort == "id":
        args.sort = "index"

    """ do stuff """
    if args.command == "coach":
        """ toggle coach mode """
        if len(args.option) != 1:
            print("Bad input")
            return
        cf_coach.coach_mode(args.option[0] == "on")

    elif args.command == "gym" or args.command == "con":
        """ set contest """
        """ check if bad input """
        if len(args.option) > 1:
            print("Bad input")
            return
        """ keep going """
        contest = None
        if len(args.option) == 1:
            contest = args.option[0]
        else:
            contest = input("Contest/Gym number: ")
        contestfile = open(contest_loc, "w")
        contestfile.write(contest)
        contestfile.close()
        if len(contest) >= 6:
            print("Gym set to " + contest)
        else:
            print("Contest set to " + contest)

    elif args.command == "ext":
        if len(args.option) > 1:
            print("Bad input")
            return
        defext = None
        if len(args.option) == 1:
            defext = args.option[0]
        else:
            defext = input("Default file extension: ")
        defext_loc = os.path.join(os.path.dirname(__file__), "default_ext");
        extfile = open(defext_loc, "w")
        extfile.write(defext)
        extfile.close()
        print("Default extension set to " + defext)

    elif args.command == "info":
        handle = cf_login.get_secret(False)
        print("handle: " + handle)
        print("contestID: " + str(defaultcontest))

    elif args.command == "login":
        """ set login info """
        if len(args.option) == 0:
            cf_login.set_login()
        elif len(args.option) == 1:
            cf_login.set_login(args.option[0])
        else:
            print("Bad Input")
            return

    elif args.command == "peek":
        """ look at last submission """
        cf_submit.peek(cf_login.get_secret(False))

    elif args.command == "watch":
        cf_submit.watch(cf_login.get_secret(False))

    elif args.command == "time":
        if args.contest is None:
            print_time(defaultcontest)
        else:
            print_time(args.contest)

    elif args.command == "standings":
        """ look at standings """
        if args.contest is None:
            print_standings(defaultcontest, args.verbose, args.top, args.sort, args.all)
        else:
            print_standings(args.contest, args.verbose, args.top, args.sort, args.all)

    elif args.command == "problems":
        """ look at problem stats """
        if args.contest is None:
            print_problems(defaultcontest, args.verbose, args.sort)
        else:
            print_problems(args.contest, args.verbose, args.sort)

    elif args.command == "submit":
        """ get default ext """
        defextension = None
        defext_loc = os.path.join(os.path.dirname(__file__), "default_ext");
        if os.path.isfile(defext_loc):
            extfile = open(defext_loc, "r")
            defextension = extfile.read().rstrip('\n')
            extfile.close()
        """ get handle and password """
        defaulthandle, defaultpass = cf_login.get_secret(True)
        """ open browser """
        browser = cf_login.login()
        if args.contest is not None:
            defaultcontest = args.contest
        if browser is not None:
            cf_submit.submit_files(
                    browser, defaulthandle, defaultcontest, args.prob, defextension,
                    args.lang, args.option, args.watch, args.guru
            )

    elif args.command == "test":
        cf_test.test(args.option, args.verbose)

    else:
        print("UNKNOWN COMMAND")


""" END """
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("")
        sys.exit(0)
