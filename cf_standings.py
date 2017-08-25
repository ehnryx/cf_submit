import sys
import requests
import json
import re
from bs4 import BeautifulSoup
from prettytable import PrettyTable

""" print friends standings in specified contest """
""" parse html """
""" gym contest """
def print_st(raw_html, verbose):
	""" set default encoding """
	reload(sys)
	sys.setdefaultencoding("utf-8")

	""" get standings table """
	mellon = raw_html.find_all("table", class_="standings")[0].find_all("tr")
	
	standings = PrettyTable()

	""" get header """
	header = []
	if verbose: 
		for hcell in mellon[0].find_all("th")[:4]:
			hcellstr = str(hcell.get_text(strip=True))
			if hcellstr == "*":
				hcellstr = "Hacks"
			header.append(hcellstr)
	else: 
		for hcell in mellon[0].find_all("th")[1:3]:
			header.append(str(hcell.get_text(strip=True)))
	for hcell in mellon[0].find_all("a"):
		header.append(str(hcell.get_text(strip=True)))
	standings.field_names = header

	""" get rows """
	for ami in mellon[1:-1]:
		virtual = True
		row = ami.find_all("td")
		tablerow = []
		""" get place """
		""" this cell has problems """
		problemcell = str(row[0].get_text(strip=True))
		if len(problemcell) == 0:
			virtual = False
		if verbose:
			tablerow.append(re.sub(r'[^\x00-\x7F]+', ' ', problemcell))
		""" get name """
		party = str(row[1].get_text(strip=True))
		if verbose:
			partyname = []
			if party.find(':') != -1:
				party = party.split(':')
				partyname.append(party[0]+":")
				for member in party[1].split(','):
					partyname.append(member)
				party = '\n'.join(partyname)
		else:
			party = party.split(':')[0]
		tablerow.append(party)
		""" get points or number of solves """
		tablerow.append(str(row[2].get_text(strip=True)))
		""" get penalty or hacks """
		if verbose:
			tablerow.append(str(row[3].get_text(strip=True)))
		""" get problem submissions """
		for cell in row[4:]:
			problemres = str(cell.get_text(strip=True))
			if virtual and len(problemres) > 5:
				if verbose:
					problemres = (problemres[:-5] + '\n' + problemres[-5:])
				else:
					problemres = problemres[:-5]
			else:
				problemres = problemres.replace("-", "WA-")
			tablerow.append(problemres)
		standings.add_row(tablerow)
	
	""" print standings """
	if verbose:
		standings.hrules = True
	print standings
	

def print_top(contest, top):
	print "work in progress"
	print "request for contestid=" + contest + " top " + str(top)
	return
