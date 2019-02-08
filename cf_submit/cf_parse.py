import os
from subprocess import Popen
from robobrowser import RoboBrowser

from .cf_colors import colors


def parse(group, contest, problem):
    Popen(["rm", "-rf", "files"]).wait()
    Popen(["mkdir", "-p", "files"]).wait()
    print("%sImporting samples of problem %s...%s" %
          (colors.WARNING, str(contest + problem), colors.ENDC))
    j = 0
    try:
        browser = RoboBrowser(parser="lxml")
        if group is None:
            browser.open("https://codeforces.com/contest/%s/problem/%s"
                         % (contest, problem))
        else:
            browser.open("https://codeforces.com/group/%s/contest/%s/problem/%s"
                         % (group, contest, problem))
        page = browser.parsed
        sample_test = page.find("div", class_="sample-test")
        inputs = sample_test.find_all("div", class_="input")
        for i in inputs:
            input_text = i.find("pre")
            input_text = str(input_text).replace(
                '<br/>', '\n').replace('<pre>', '').replace('</pre>', '')
            create_file(input_text.strip(), "test%d.in" % (j))
            j += 1
        outputs = sample_test.find_all("div", class_="output")
        j = 0
        for i in outputs:
            output_text = i.find("pre")
            output_text = str(output_text).replace(
                '<br/>', '\n').replace('<pre>', '').replace('</pre>', '')
            create_file(output_text.strip(), "test%d.ans" % (j))
            j += 1
    except Exception:
        print("%sError, try in few minutes!!%s" %
              (colors.FAIL, colors.ENDC))
        return
    print("%s%d samples imported successfully!%s" %
          (colors.OKGREEN, j, colors.ENDC))


def create_file(source, file_name):
    for_hak_source = open(os.path.join("files", file_name), "w")
    for_hak_source.write(source)
    for_hak_source.close()
