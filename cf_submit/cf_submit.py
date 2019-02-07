import sys
import time
import json
import re
import requests

from .cf_colors import colors

# submissions


def get_submission_data(handle):
    req = requests.get(
        "http://codeforces.com/api/user.status?handle=%s&from=1&count=1" % (handle))
    content = req.content.decode()
    js = json.loads(content)
    if "status" not in js or js["status"] != "OK":
        print("Connection Error!")
    res = js["result"][0]
    # check if verdict exists (in queue if not)
    if "verdict" not in res:
        res["verdict"] = "IN QUEUE"
    return res["id"], res["problem"], res["verdict"], res["passedTestCount"], res["timeConsumedMillis"], res["memoryConsumedBytes"]


# look at last submission

def peek(handle):
    id_, probject, verdict, passedTests, timeCon, memCon = get_submission_data(
        handle)
    problem = str(probject["contestId"]) + str(probject["index"])
    if verdict == "TESTING":
        print("submission %s to problem %s: %s"
              % (str(id_), problem, verdict))
    else:
        if verdict != "OK":
            print("submission %s to problem %s: %s on test %s\nTime: %sms \nMemory: %sKb"
                  % (str(id_), problem, verdict, str(1 + passedTests), str(timeCon), str(memCon / 1024)))
        else:
            print("submission %s to problem %s: %s! passed all %s tests\nTime: %sms \nMemory: %sKb"
                  % (str(id_), problem, verdict, str(passedTests), str(timeCon), str(memCon / 1024)))


# watch last submission

def watch(handle):
    spinner = {0: "◐", 1: "◓", 2: "◑", 3: "◒"}

    count = 0
    while True:
        id_, probject, verdict, passedTests, timeCon, memCon = get_submission_data(
            handle)
        if "contestId" not in probject:
            probject["contestId"] = "guru"
        problem = str(probject["contestId"]) + str(probject["index"])
        if verdict != "TESTING" and verdict != "IN QUEUE":
            if verdict != "OK":
                sys.stdout.write("\rsubmission %s to problem %s: %s on test %s\nTime: %sms \nMemory: %sKb"
                                 % (str(id_), problem, verdict, str(1 + passedTests), str(timeCon), str(memCon / 1024)))
            else:
                sys.stdout.write("\rsubmission %s to problem %s: %s! passed all %s tests\nTime: %sms \nMemory: %sKb"
                                 % (str(id_), problem, verdict, str(passedTests), str(timeCon), str(memCon / 1024)))
            sys.stdout.flush()
            break
        else:
            sys.stdout.write("\rsubmission %s to problem %s: %s ....... %s"
                             % (str(id_), problem, verdict, spinner[count]))
            sys.stdout.flush()
            count = (count + 1) % 4
        time.sleep(0.25)
    print('\a')


# submit problem

def submit_problem(browser, group, contest, lang, source, guru):
    # get form
    submission = browser.get_form(class_="submit-form")
    if submission is None:
        print("Cannot find problem")
        return False

    # submit form
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
    elif lang == "d":
        langcode = "28"
    elif lang == "py":
        # python 2.7.12
        # langcode = "7"
        # python 3.5.2
        langcode = "31"
    elif lang == "rb":
        # Ruby 2.0.0p645
        langcode = "8"
    elif lang == "java":
        # Java 1.8.0_112
        langcode = "36"
    elif lang == "scala":
        langcode = "20"
    elif lang == "rs":
        langcode = "49"
    elif lang == "php":
        langcode = "6"
    else:
        print("Unknown Language")
        return False
    submission["programTypeId"] = langcode

    # check acmsguru
    if guru != -1:
        submission["submittedProblemCode"] = guru

    browser.submit_form(submission)

    # check if good
    if (guru != -1 and browser.url[-7:] != "/status") or (guru == -1 and browser.url[-3:] != "/my"):
        print("Failed to submit code")
        print(" @ %s" % (str(browser.url)))
        return False
    print("Code submitted properly")

    # now get time
    countdown_timer = browser.parsed.find_all(
        "span", class_="contest-state-regular countdown before-contest-" + contest + "-finish")
    if len(countdown_timer) > 0:
        print("%sTIME LEFT: %s%s" %
              (colors.BOLD, str(countdown_timer[0].get_text(strip=True)), colors.ENDC))

    return True


# submit problem


def submit(browser, handle, group, contest, problem, lang, source, show, guru):
    if guru:
        print("Submitting to acmsguru %s as %s"
              % (problem, handle))
    elif group is not None:
        print("Submitting to problem %s%s in group %s as %s"
              % (contest, problem.upper(), group, handle))
    else:
        print("Submitting to problem %s%s as %s"
              % (contest, problem.upper(), handle))

    pid = -1
    if guru:
        browser.open("http://codeforces.com/problemsets/acmsguru/submit")
        pid = problem
    elif group is not None:
        browser.open("http://codeforces.com/group/%s/contest/%s/submit/%s"
                     % (group, contest, problem.upper()))
    elif len(contest) >= 6:
        browser.open("http://codeforces.com/gym/%s/submit/%s"
                     % (contest, problem.upper()))
    else:
        browser.open("http://codeforces.com/contest/%s/submit/%s"
                     % (contest, problem.upper()))

    # show submission
    if submit_problem(browser, group, contest, lang, source, pid) and show:
        watch(handle)


# submit, possibly len(args) > 1


def submit_files(browser, defaulthandle, defaultgroup, defaultcontest, defaultprob, defext, defaultlang, args, show, guru):
    # if len == 0, query for file
    if len(args) == 0:
        args.append(input('File to submit: '))

    for source in args:
        # split file name
        info = source.split('.')
        # single filename
        if source.find('.') == -1:
            info.append(defext)
            source += "." + defext

        # check language
        if defaultlang is not None:
            info[-1] = defaultlang

        # submit problem
        if defaultprob is not None:
            if len(defaultprob) == 1:
                # letter only
                submit(browser, defaulthandle, defaultgroup, defaultcontest,
                       defaultprob, info[-1], source, show, guru)
            elif len(defaultprob) == 2:
                # letter + number (?)
                submit(browser, defaulthandle, defaultgroup, defaultcontest,
                       defaultprob, info[-1], source, show, guru)
            else:
                #  parse string
                splitted = re.split(r"(\D+)", defaultprob)
                if len(splitted) == 3 and len(splitted[1]) == 1 and len(splitted[2]) == 0:
                    # probably a good string
                    submit(browser, defaulthandle, defaultgroup,
                           splitted[0], splitted[1], info[-1], source, show, guru)
                else:
                    print("cannot understand the problem specified")

        elif len(info) == 2:
            if guru:
                # ACMSGURU
                submit(browser, defaulthandle, defaultgroup,
                       defaultcontest, info[0], info[1], source, show, guru)
            else:
                # CODEFORCES
                # try to parse info[0]
                if info[0][:2].lower() == "cf":
                    # remove the cf
                    info[0] = info[0][2:]
                if len(info[0]) == 1:
                    # only the letter, use default contest
                    submit(browser, defaulthandle, defaultgroup,
                           defaultcontest, info[0], info[1], source, show, guru)
                else:
                    # contest is included, so parse
                    splitted = re.split(r"(\D+)", info[0])
                    if len(splitted) == 3 and len(splitted[1]) == 1 and len(splitted[2]) == 0:
                        # probably good string ?
                        submit(browser, defaulthandle, defaultgroup,
                               splitted[0], splitted[1], info[1], source, show, guru)
                    else:
                        print(
                            "cannot parse filename, specify problem with -p or --prob")

        else:
            print("cannot parse filename, specify problem with -p or --prob")
