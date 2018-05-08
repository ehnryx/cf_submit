import sys
import json
import requests
from robobrowser import RoboBrowser
import cf_login

def coach_mode(coach_on):
	browser = cf_login.login()
	browser.open("http://codeforces.com/gyms")
	raw_html = str(browser.parsed)
	if coach_on:
		if raw_html.find("Enable coach mode") != -1:
			toggle_form = browser.get_form(class_="toggleGymContestsManagerEnabled")
			browser.submit_form(toggle_form)
			print("Coach Mode On")
		else:
			print("Coach Mode is already On")
	else:
		if raw_html.find("Disable coach mode") != -1:
			toggle_form = browser.get_form(class_="toggleGymContestsManagerEnabled")
			browser.submit_form(toggle_form)
			print("Coach Mode Off")
		else:
			print("Coach Mode is already Off")
	return
