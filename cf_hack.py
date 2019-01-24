import os
import re
import time
import javalang
from subprocess import Popen
from robobrowser import RoboBrowser

import cf_login
from colors import colors

dir_path = os.getcwd()


# Hack problems

def hack(contest, hack_test, submission_id):
    browser = cf_login.login()
    browser.open("https://codeforces.com/contest/" +
                 contest + "/challenge/" + str(submission_id))
    hack_form = browser.get_form(class_="challenge-form")
    hack_form["testcaseFromFile"] = hack_test
    browser.submit_form(hack_form)


def begin_hack(contest, problem, generator, checker, correct_solution, test_number):
    global file_name
    hacked_solutions = 0
    tried_solutions = 0

    # Preparing Workspace
    init_workspace_process = Popen(
        ["/bin/bash", os.path.join(os.path.dirname(__file__), "init_workspace.sh"), generator,
         checker, correct_solution])
    tried_submissions_list = open(os.path.join(
        os.path.dirname(__file__), "tried_submissions"), "r")

    list_str = tried_submissions_list.read().strip()
    tried_submissions = list()
    if list_str != "":
        tried_submissions = list(map(int, list_str.split(' ')))
    tried_submissions_list = open(os.path.join(
        os.path.dirname(__file__), "tried_submissions"), "a")
    init_workspace_process.wait()

    browser = RoboBrowser(parser="lxml")
    browser.open("https://codeforces.com/contest/" +
                 contest + "/status/" + problem.upper())
    max_pages = int(browser.find_all(class_="page-index")[-1].text)
    print("\n%sHappy Hacking 3:) - max pages : %d%s" %
          (colors.HEADER, max_pages, colors.ENDC))
    for i in range(max_pages, 0, -1):
        try:
            browser = RoboBrowser(parser="lxml")
            browser.open("https://codeforces.com/contest/%s/status/%s/page/%d?order=BY_ARRIVED_DESC"
                         % (contest, problem.upper(), i))
            submissions = browser.find_all(
                "table", class_="status-frame-datatable")[0].find_all("tr")[1:]
            for submission in submissions:
                submission_id = int(submission.find(
                    "td", class_="id-cell").find("a").text)
                tried_solutions = tried_solutions + 1
                if submission_id in tried_submissions:
                    print("\n%sSubmission %d on page %d/%d already tried!!%s" %
                          (colors.WARNING, submission_id, i, max_pages, colors.ENDC))
                    continue
                tried_submissions_list.write(str(submission_id) + " ")
                tried_submissions_list.flush()
                language = submission.find_all(
                    "td")[4].text.strip().replace(" ", "")
                browser = RoboBrowser(parser="lxml")
                browser.open(
                    "http://codeforces.com/contest/%s/submission/%d" % (contest, submission_id))
                if len(browser.find_all("pre", class_="program-source")) > 0:
                    source = browser.find_all(
                        "pre", class_="program-source")[0].text
                    file_name = create_file(source, language)
                    if file_name == "":
                        continue
                    print("\n%sHacked : %d, %sFailed : %d, %sTotal : %d%s"
                          % (colors.OKGREEN, hacked_solutions, colors.FAIL,
                             tried_solutions-hacked_solutions,
                             colors.OKBLUE, tried_solutions, colors.ENDC))
                    print("%sTrying to hack a %s solution - %d on page %d/%d...%s"
                          % (colors.HEADER, language, submission_id, i, max_pages, colors.ENDC))

                    hack_process = Popen(
                        ["timeout", "120", os.path.join(os.path.dirname(__file__), "hack_prob.sh"),
                         generator, checker, correct_solution, file_name, language.replace(" ", ""), str(test_number)])
                    hack_process.wait()
                    exit_code = hack_process.returncode
                    if exit_code in [0, 255]:
                        print("%sSorry, can't hack this solution x/" %
                              (colors.FAIL))
                    else:
                        test_hack_loc = os.path.join(
                            dir_path, "workspace", "failed.txt")
                        if os.path.isfile(test_hack_loc):
                            print("%sHope that will win 3:)%s" %
                                  (colors.OKGREEN, colors.ENDC))
                            hacked_solutions = hacked_solutions + 1
                            hack(contest, test_hack_loc, submission_id)
        except KeyboardInterrupt:
            time.sleep(2)
            break
        except Exception:
            continue
    print("\n%sRESULT => %sHacked : %d, %sFailed : %d, %sTotal : %d"
          % (colors.HEADER, colors.OKGREEN, hacked_solutions, colors.FAIL,
             tried_solutions-hacked_solutions, colors.OKBLUE, tried_solutions))


def create_file(source, language):
    global file_name
    if re.match(r"(.)*\+\+(.)*", language):
        file_name = "noncorrect.cpp"
    elif re.match(r"(.)*GNU(.)*", language):
        file_name = "noncorrect.c"
    elif re.match(r"(.)*Java(.)*", language):
        try:
            tree = javalang.parse.parse(source)
            name = next(klass.name for klass in tree.types
                        if isinstance(klass, javalang.tree.ClassDeclaration)
                        for m in klass.methods
                        if m.name == 'main' and m.modifiers.issuperset({'public', 'static'}))
            file_name = name + ".java"
        except Exception:
            return ""
    elif re.match(r"(.)*Py(.)*", language):
        file_name = "noncorrect.py"
    else:
        return ""

    for_hak_source = open(os.path.join(dir_path, "workspace", file_name), "w")
    for_hak_source.write(source)
    for_hak_source.close()
    return file_name
