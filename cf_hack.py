
# Hack problems

def hack(browser, handle, contest, problem, source):
    browser.open("https://codeforces.com/contest/" + contest + "/status/" + problem.upper())
    max_pages = int(browser.find_all(class_="page-index")[-1].text)
    begin_hack(browser, handle, contest, problem, source, max_pages)


def begin_hack(browser, handle, contest, problem, source, max_pages):
    print("Happy Hacking 3:)")
    i = 1
    while i <= max_pages:
        browser.open("https://codeforces.com/contest/" + contest + "/status/" + problem.upper() + "/page/" + str(
            i) + "?order=BY_PROGRAM_LENGTH_ASC")
        submissions = browser.find_all(class_="id-cell")
        for submission in submissions:
            submission_id = int(submission.text)
            browser.open("https://codeforces.com/contest/" + contest + "/challenge/" + str(submission_id))
            hack_form = browser.get_form(class_="challenge-form")
            hack_form["testcaseFromFile"] = source
            browser.submit_form(hack_form)
        i += 1
