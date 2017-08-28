import sys
import requests
import json
import re
from prettytable import PrettyTable
import colours

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
			if party.count(':') == 2:
				""" split at first colon """
				team.append(party[:party.find(':')+1])
				party = party[party.find(':')+1:]
				""" split rest of team members """
				for member in party[:-5].split(','):
					team.append(member)
				team.append(party[-5:])
				party = '\n'.join(team)
			elif party.count(':') == 1:
				""" check if virtual colon or other """
				if party[-3] == ':':
					""" virtual time colon """
					party = '\n'.join([party[:-5], party[-5:]])
				else:
					""" team name colon """
					team.append(party[:party.find(':')])
					if party[-1] == '#':
						team[-1] += "#"
						party = party[:-1]
					team[-1] += ":"
					for membergroup in party[party.find(':')+1:].split(','):
						for member in membergroup.split():
							team.append(member)
					party = '\n'.join(team)
		else:
			""" check type """
			if party.count(':') > 1:
				""" check for # """
				tail = ""
				if party[-1] == '#':
					tail = "#"
				party = party.split(':')[0]
				party += tail
			elif party.count(':') == 1:
				if party[-3] == ':':
					party = party[:-5]
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

