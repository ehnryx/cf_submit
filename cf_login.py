import os
import random
import getpass
from robobrowser import RoboBrowser

""" converter """
def decode(s):
	res = ""
	length = len(s)
	i = 0
	while i < length:
		jump = ord(s[i])-ord('7')
		temp = 0
		for j in range (0, jump):
			temp += ord(s[i+j+1]) - ord('F')
		res += str(chr(temp))
		i += jump + 1
	return res

def encode(s):
	res = ""
	length = len(s)
	for i in range (0, length):
		jump = random.randint(1, 20)
		res += str(chr(jump + ord('7')))
		curr = ord(s[i])
		for j in range (0, jump-1):
			temp = random.randint(0, min(curr, 2+int(curr/(jump-j))))
			res += str(chr(temp + ord('F')))
			curr -= temp
		res += str(chr(curr + ord('F')))
	return res

def get_secret(inclupass):
	handle = None
	password = None
	if os.path.isfile("/home/d/d0b1b/Tools/cf_submit/secret"):
		secretfile = open("/home/d/d0b1b/Tools/cf_submit/secret", "r")
		rawdata = secretfile.read().rstrip('\n').split()
		handle = decode(rawdata[0])
		if inclupass:
			password = decode(rawdata[1])
		secretfile.close()
	if inclupass:
		return handle, password
	else:
		return handle

""" set login """
def set_login(handle=None):
	if handle is None:
		handle = raw_input("Handle: ")
	password = getpass.getpass("Password: ")

	browser = RoboBrowser(parser = "lxml")
	browser.open("http://codeforces.com/enter")
	enter_form = browser.get_form("enterForm")
	enter_form["handle"] = handle
	enter_form["password"] = password
	browser.submit_form(enter_form)

	checks = list(map(lambda x: x.getText()[1:].strip(), 
		browser.select('div.caption.titled')))
	if handle not in checks:
		print("Login Failed.")
		return
	else:
		secretfile = open("/home/d/d0b1b/Tools/cf_submit/secret", "w")
		secretfile.write(encode(handle) + " " + encode(password))
		secretfile.close()
		print ("Successfully logged in as " + handle)

