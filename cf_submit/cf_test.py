import os
import glob
from subprocess import Popen

from .cf_colors import colors


def test(source, lang):
    info = source.split('.')
    if lang is None:
        lang = info[-1]
    if lang == "py":
        print("%sPlease specify the version of python : py2 or py3%s" %
              (colors.FAIL, colors.ENDC))
        return
    print("%sCompiling your %s solution..." %
          (colors.OKBLUE, lang))
    comp(source, lang, info)

    print("Executing...%s" % colors.ENDC)
    i = 1
    success = 0
    failed = 0
    for file_name in glob.iglob('files/test*.in'):
        with open(file_name, "r") as input_file:
            with open(file_name.replace(".in", ".out"), "w") as output_file:
                print("%s#################### TEST %d ####################%s\n" %
                      (colors.WARNING, i, colors.ENDC))
                i += 1
                execute(source, lang, info, input_file, output_file)
                proccess = Popen(["cf_checker", file_name,
                                  file_name.replace(".in", ".out"), file_name.replace(".in", ".ans")])
                proccess.wait(timeout=5)
                exit_code = proccess.returncode
                print("\n%sInput:%s" % (colors.OKBLUE, colors.ENDC))
                print(open(file_name, 'r').read(), "\n")
                if exit_code == 0:
                    success += 1
                else:
                    print("%sExpected:%s" % (colors.OKBLUE, colors.ENDC))
                    print(
                        str(open(file_name.replace(".in", ".ans"), 'r').read()).strip(), "\n")
                    failed += 1
                print("%sOutput:%s" % (colors.OKBLUE, colors.ENDC))
                print(
                    str(open(file_name.replace(".in", ".out"), 'r').read()).strip(), "\n")

    print("%s################################################%s\n" %
          (colors.WARNING, colors.ENDC))
    print("%sSuccess: %d, %sFailed: %d%s" %
          (colors.OKGREEN, success, colors.FAIL, failed, colors.ENDC))


def execute(source, lang, info, input_file, output_file):
    if lang == "cpp" or lang == "c":
        cmd = "./%s" % (info[0])
    elif lang == "java":
        cmd = "java %s" % (info[0])
    elif lang == "py2":
        cmd = "python2 %s" % (source)
    elif lang == "py3":
        cmd = "python3 %s" % (source)
    else:
        print("Sorry language not supported!")
        exit(-1)
    Popen(cmd, stdin=input_file,
          stdout=output_file, shell=True).wait()


def comp(source, lang, info):
    if lang == "cpp":
        Popen("g++ %s -O2 -o %s" % (source, info[0]), shell=True).wait()
    elif lang == "c":
        Popen("gcc %s -O2 -o %s" % (source, info[0]), shell=True).wait()
    elif lang == "java":
        Popen("javac %s" % (source), shell=True).wait()
