import os
import re
import javalang
from subprocess import Popen
from robobrowser import RoboBrowser

import cf_login

dir_path = os.getcwd()


# Hack problems

def hack(contest, hack_test, submission_id):
    browser = cf_login.login()
    browser.open("https://codeforces.com/contest/" + contest + "/challenge/" + str(submission_id))
    hack_form = browser.get_form(class_="challenge-form")
    hack_form["testcaseFromFile"] = hack_test
    browser.submit_form(hack_form)


def begin_hack(contest, problem, generator, checker, correct_solution, test_number):
    global file_name
    init_workspace_process = Popen(
        ["/bin/bash", os.path.join(os.path.dirname(__file__), "init_workspace.sh"), generator, checker,
         correct_solution])
    tried_submissions_list = open(os.path.join(os.path.dirname(__file__), "tried_submissions"), "r")
    list_str = tried_submissions_list.read().strip()
    tried_submissions = list()
    if list_str != "":
        tried_submissions = list(map(int, list_str.split(' ')))
    tried_submissions_list = open(os.path.join(os.path.dirname(__file__), "tried_submissions"), "a")
    init_workspace_process.wait()

    browser = RoboBrowser(parser="lxml")
    browser.open("https://codeforces.com/contest/" + contest + "/status/" + problem.upper())
    max_pages = int(browser.find_all(class_="page-index")[-1].text)
    print("Happy Hacking 3:) - max pages : " + str(max_pages))
    for i in range(1, max_pages):
        try:
            browser = RoboBrowser(parser="lxml")
            browser.open("https://codeforces.com/contest/" + contest + "/status/" + problem.upper() + "/page/" + str(
                i) + "?order=BY_PROGRAM_LENGTH_ASC")
            submissions = browser.find_all("table", class_="status-frame-datatable")[0].find_all("tr")[1:]
            for submission in submissions:
                submission_id = int(submission.find("td", class_="id-cell").find("a").text)
                if submission_id in tried_submissions:
                    print(str(submission_id) + " already tried!!")
                    continue
                tried_submissions_list.write(str(submission_id) + " ")
                tried_submissions_list.flush()
                language = submission.find_all("td")[4].text.strip().replace(" ", "")
                browser = RoboBrowser(parser="lxml")
                browser.open("http://codeforces.com/contest/" + contest + "/submission/" + str(submission_id))
                if len(browser.find_all("pre", class_="program-source")) > 0:
                    source = browser.find_all("pre", class_="program-source")[0].text
                    file_name = create_file(source, language)
                    if file_name == "":
                        continue
                    print("\nTrying to hack a " + language + " solution - " + str(submission_id) + " on page " + str(
                        i) + "...")
                    hack_process = Popen(
                        ["timeout", "10", os.path.join(os.path.dirname(__file__), "hack_prob.sh"),
                         generator, checker, correct_solution, file_name, language.replace(" ", ""), str(test_number)])
                    hack_process.wait()
                    exit_code = hack_process.returncode
                    if exit_code in [0, 255]:
                        print("Sorry, can't hack this solution x/")
                    else:
                        test_hack_loc = os.path.join(dir_path, "workspace", "failed.txt")
                        if os.path.isfile(test_hack_loc):
                            print("Hope that will win 3:)")
                            hack(contest, test_hack_loc, submission_id)
        except Exception:
            continue


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
