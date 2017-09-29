import os
from subprocess import Popen

def test(args):
	if len(args) == 0:
		args.append(raw_input("Problem to test: "))
	for prob in args:
		testsc = Popen(["/bin/bash", "test_prob.sh", prob.lower()])
		testsc.wait()

	print "nothing here"
	return
