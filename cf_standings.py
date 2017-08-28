import sys
import requests
import json
import re
from prettytable import PrettyTable
import colours

def makeascii(s):
	return re.sub(r'[^\x00-\x7f]',r'?',s)

""" print friends standings in specified contest """
""" parse html """
""" gym contest """
def print_st(raw_html, verbose, top):
	""" set default encoding """
	reload(sys)
	sys.setdefaultencoding("utf-8")

	""" get standings table """
	mellon = raw_html.find_all("table", class_="standings")[0].find_all("tr")
	
	standings = PrettyTable()

	""" get header """
	firstpart = len(mellon[0].find_all("th")) - len(mellon[0].find_all("a"))
	header = []
	if verbose: 
		for hcell in mellon[0].find_all("th")[:firstpart]:
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
	if top is None:
		rankrowlist = mellon[1:-1]
	else:
		rankrowlist = mellon[1:top+1]
	""" iterate """
	for ami in rankrowlist:
		virtual = True
		row = ami.find_all("td")
		tablerow = []
		""" get place """
		""" this cell has problems """
		rank = str(row[0].get_text(strip=True))
		if len(rank) == 0:
			virtual = False
		if verbose:
			if rank.find(')') != -1:
				rank = rank[rank.find('(')+1:rank.find(')')]
			tablerow.append(rank)
		""" get name """
		""" TODO: check whether virtual or actual
		separate time for virtual contests """
		party = str(row[1].get_text(strip=True))
		if verbose:
			team = []
			""" check if virtual time colon """
			virtualtime = None
			if party[-3] == ':':
				virtualtime = party[-5:]
				party = party[:-5]
			""" check if there are still colons left
			if yes, split at last colon """
			if party.count(':') > 0:
				""" check for '#' """
				tail = ""
				if party[-1] == '#':
					tail = "#"
					party = party[:-1]
				""" split """ 
				party = party.split(':')
				""" get first part (team name) """
				teamname = party[0]
				for partypart in party[1:-1]:
					teamname += ":" + partypart
				if len(teamname+tail) > 24:
					print teamname[:20]
					teamname = teamname[:20] + "..."
				teamname += tail + ":"
				team.append(teamname)
				""" split rest of team members """
				for member in party[-1].split(','):
					team.append(member.strip())
			else:
				team.append(party)
			""" append time if it exists"""
			if virtualtime is not None:
				team.append(virtualtime)
			""" join party """
			party = '\n'.join(team)
		else:
			if party[-3] == ':':
				party = party[:-5]
			if party.count(':') > 0:
				tail = ""
				if party[-1] == '#':
					tail = "#"
					party = party[:-1]
				""" split """
				party = party.split(':')
				teamname = party[0]
				for partypart in party[1:-1]:
					teamname += ":" + partypart
				teamname += tail
				party = teamname
		tablerow.append(makeascii(party))
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
		if "Penalty" in standings.align:
			standings.align["Penalty"] = "r"
	standings.align["Who"] = "l"
	standings.align["="] = "r"
	print standings

	""" first check if countdown """
	#boldstart = "\033[1m"
	#boldend = "\033[0;0m"
	countdown_timer = raw_html.find_all("span", class_="countdown")
	if len(countdown_timer) > 0:
		print colours.bold() + "TIME LEFT: " + str(countdown_timer[0].get_text(strip=True)) + colours.reset()

