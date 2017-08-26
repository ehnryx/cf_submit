import sys
from prettytable import PrettyTable

def print_prob(raw_html, verbose):
	""" set default encoding """
	reload(sys)
	sys.setdefaultencoding("utf-8")

	stats = PrettyTable()

	""" header """
	header = ["#", "Name", "Solves"]
	stats.field_names = header
	
	""" get standings table """
	probraw = raw_html.find_all("table", class_="problems")[0].find_all("tr")
	for row in probraw[1:]:
		tablerow = []
		cell = row.find_all("td")
		tablerow.append(str(cell[0].get_text(strip=True)))
		tablerow.append(str(cell[1].find("a").get_text(strip=True)))
		tablerow.append(str(cell[3].get_text(strip=True))[1:])
		stats.add_row(tablerow)

	stats.hrules = True
	stats.align["Name"] = "l"
	print stats

def print_casual(contest, verbose):
	print "work in progress"
	print "request: contest="+contest + " verbose="+str(verbose)

