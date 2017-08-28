import sys
import time
import json
import requests
import colours

""" submissions """ 
def get_submission_data(handle):
	req = requests.get("http://codeforces.com/api/user.status?handle={}&from=1&count=1".format(handle))
	content = req.content.decode()
	js = json.loads(content)
	if "status" not in js or js["status"] != "OK":
		print("Connection Error!")
	res = js["result"][0]
	# check if verdict exists (in queue if not)
	if "verdict" not in res:
		res["verdict"] = "IN QUEUE"
	return res["id"], res["problem"], res["verdict"], res["passedTestCount"], res["timeConsumedMillis"], res["memoryConsumedBytes"]

""" look at last submission """
def peek(handle):
	id_, probject, verdict, passedTests, timeCon, memCon = get_submission_data(handle)
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
		# GNU G++14 6.2.0
		langcode = "50"
		# GNU G++11 5.1.0
		# langcode = "42"
	elif lang == "c":
		# GNU GCC C11 5.1.0
		langcode = "43"
	elif lang == "py":
		# python 2.7.12
		langcode = "7"
		# python 3.5.2
		# langcode = "31"
	elif lang == "java": 
		# Java 1.8.0_112
		langcode = "36"
	else: 
		print("Unknown Language")
		return False
	submission["programTypeId"] = langcode

	browser.submit_form(submission)
	
	""" check if good """
	if browser.url[-3:] != "/my":
		print("Failed to submit code")
		return False
	print("Code submitted properly")

	""" now get time """
	countdown_timer = browser.parsed.find_all("span", class_="contest-state-regular countdown before-contest-"+contest+"-finish")
	if len(countdown_timer) > 0:
		print colours.bold() + "TIME LEFT: " + str(countdown_timer[0].get_text(strip=True)) + colours.reset()
	
	return True

