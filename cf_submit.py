import sys
import time
import json
import re
import requests
import colours

""" submissions """ 
def get_submission_data(handle):
    req = requests.get("https://codeforces.com/api/user.status?handle={}&from=1&count=1".format(handle))
    content = req.content.decode()
    js = json.loads(content)
    if "status" not in js or js["status"] != "OK":
        print("Connection Error!")
    if "result" not in js:
        return "?", "?", "?", "?", "?", "?"
    res = js["result"][0]
    # check if verdict exists (in queue if not)
    if "verdict" not in res:
        res["verdict"] = "IN QUEUE"
    return res["id"], res["problem"], res["verdict"], res["passedTestCount"], res["timeConsumedMillis"], res["memoryConsumedBytes"]

""" look at last submission """
def peek(handle):
    id_, probject, verdict, passedTests, timeCon, memCon = get_submission_data(handle)
    if id_ == "?":
        sys.stdout.write("\r" + "some error occurred")
        sys.stdout.flush()
        return
    problem = str(probject["contestId"])+str(probject["index"])
    if verdict == "TESTING":
        print("submission "+str(id_) + " to problem "+problem + ": "+verdict)
    else:
        if verdict != "OK":
            print("submission "+str(id_) + " to problem "+problem + ": "+verdict + " on test "+str(1+passedTests) + "\n" + "Time: "+str(timeCon)+"ms \n" + "Memory: "+str(memCon/1024)+"Kb")
        else:
            print("submission "+str(id_) + " to problem " + problem + ": " + verdict+"! passed all " + str(passedTests) + " tests\n" + "Time: "+str(timeCon)+"ms \n" + "Memory: "+str(memCon/1024)+"Kb")

""" watch last submission """
def watch(handle):
    spinner = { 0: "-", 1: "/", 2: "\\" }
    count = 0
    while True:
        id_, probject, verdict, passedTests, timeCon, memCon = get_submission_data(handle)
        if id_ == "?":
            sys.stdout.write("\r" + "some error occurred")
            sys.stdout.flush()
            continue
        problem = str(probject["contestId"])+str(probject["index"])
        if verdict != "TESTING" and verdict != "IN QUEUE":
            if verdict != "OK": 
                sys.stdout.write("\r" + "submission "+str(id_) + " to problem " + problem + ": " + verdict + " on test "+str(1+passedTests) + "\n" + "Time: "+str(timeCon)+"ms \n" + "Memory: "+str(memCon/1024)+"Kb")
            else:
                sys.stdout.write("\r" + "submission "+str(id_) + " to problem " + problem + ": " + verdict+"! passed all " + str(passedTests) + " tests\n" + "Time: "+str(timeCon)+"ms \n" + "Memory: "+str(memCon/1024)+"Kb")
            sys.stdout.flush()
            break
        else:
            sys.stdout.write("\r" + "submission "+str(id_) + " to problem "+problem + ": "+verdict + " ....... "+spinner[count] + (' '*7))
            sys.stdout.flush()
            count = (count+1) % 3
        time.sleep(0.25)
    print('\a')


""" submit problem """
def submit_problem(browser, contest, lang, source):
    """ get form """
    submission = browser.get_form(class_="submit-form")
    if submission is None:
        print("Cannot find problem")
        return False

    """ submit form """
    submission["sourceFile"] = source
    langcode = None
    if lang == "cpp":
        # GNU G++17 9.2.0 (64 bit)
        langcode = "61"
        # GNU G++17 7.3.0
        # langcode = "54"
        # GNU G++14 6.2.0
        # langcode = "50"
        # GNU G++11 5.1.0
        # langcode = "42"
    #elif lang == "c++17":
        # GNU G++17 7.3.0
        # langcode = "54"
    elif lang == "c":
        # GNU GCC C11 5.1.0
        langcode = "43"
    elif lang == "d":
        langcode = "28"
    elif lang == "py":
        # python 2.7
        # langcode = "7"
        # python 3.6
        #langcode = "31"
    #elif lang == "pypy":
        # pypy 3.5
        langcode = "41"
    elif lang == "rb":
        # Ruby 2.0.0p645
        langcode = "8"
    elif lang == "java":
        # Java 1.8.0_112
        # langcode = "36"
        # Java 11.0.6
        langcode = "60"
    elif lang == "scala":
        langcode = "20"
    elif lang == "rs":
        langcode = "49"
    elif lang == "php":
        langcode = "6"
    elif lang == "go":
        langcode = "32"
    elif lang == "text":
        langcode = "57"
    elif lang == "kt":
        langcode = "48"
    else:
        print("Unknown Language")
        return False
    submission["programTypeId"] = langcode

    browser.submit_form(submission)

    """ check if good """
    if browser.url[-3:] != "/my":
        print("Failed to submit code")
        print(" @ " + str(browser.url))
        return False
    print("Code submitted properly")

    """ now get time """
    countdown_timer = browser.parsed.find_all("span", class_="contest-state-regular countdown before-contest-"+contest+"-finish")
    if len(countdown_timer) > 0:
        print colours.bold() + "TIME LEFT: " + str(countdown_timer[0].get_text(strip=True)) + colours.reset()
    
    return True


""" submit problem """
def submit(browser, handle, group, contest, problem, lang, source, show):
    print("Submitting to problem " + contest + problem.upper() + " as " + handle)

    if group is None:
        if len(contest) >= 6:
            url = "https://codeforces.com/gym/" + contest + "/submit/" + problem.upper()
        else:
            url = "https://codeforces.com/contest/" + contest + "/submit/" + problem.upper()
        browser.open(url)
    else:
        url = "https://codeforces.com/group/" + group + "/contest/" + contest + "/submit/" + problem.upper()
        browser.open(url)
    print("Submitting to " + url)

    """ show submission """
    if submit_problem(browser, contest, lang, source) and show:
        watch(handle)

""" submit, possibly len(args) > 1 """
def submit_files(browser, defaulthandle, group, defaultcontest, defaultprob, defext, defaultlang, args, show):
    """ if len == 0, query for file """
    if len(args) == 0:
        args.append(raw_input("File to submit: "))

    for source in args:
        """ split file name """
        info = source.split('.')
        """ single filename """
        if source.find('.') == -1:
            info.append(defext)
            source += "." + defext
        
        """ check language """
        if defaultlang is not None:
            info[-1] = defaultlang

        """ submit problem """
        if defaultprob is not None:
            if len(defaultprob) == 1:
                """ letter only """
                submit(browser, defaulthandle, group, defaultcontest, defaultprob, info[-1], source, show)
            elif len(defaultprob) == 2:
                """ letter + number (?) """
                submit(browser, defaulthandle, group, defaultcontest, defaultprob, info[-1], source, show)
            else:
                """  parse string """
                splitted = re.split('(\D+)', defaultprob)
                if len(splitted) == 3 and len(splitted[1]) == 1 and len(splitted[2]) == 0:
                    """ probably a good string """
                    submit(browser, defaulthandle, group, splitted[0], splitted[1], info[-1], source, show)
                else: 
                    print("cannot understand the problem specified")
        elif len(info) == 2:
            """ try to parse info[0] """
            if info[0][:2].lower() == "cf":
                """ remove the cf """
                info[0] = info[0][2:]
            if len(info[0]) == 1:
                """ only the letter, use default contest """
                submit(browser, defaulthandle, group, defaultcontest, info[0], info[1], source, show)
            else: 
                """ contest is included, so parse """
                splitted = re.split('(\D+)', info[0])
                if len(splitted) == 3 and len(splitted[1]) == 1 and len(splitted[2]) == 0:
                    """ probably good string ? """
                    submit(browser, defaulthandle, group, splitted[0], splitted[1], info[1], source, show)
                else:
                    print("cannot parse filename, specify problem with -p or --prob")
        else:
            print("cannot parse filename, specify problem with -p or --prob")

