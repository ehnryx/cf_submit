import os
from subprocess import Popen

def test(args, verbose):
	if len(args) == 0:
		args.append(raw_input("Problem to test: "))
	option = "None"
	if verbose:
		option = "-v"
	for prob in args:
		testsc = Popen(["/bin/bash", "test_prob.sh", prob.lower(), option])
		testsc.wait()
