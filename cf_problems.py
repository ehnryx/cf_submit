import sys
from prettytable import PrettyTable

def print_prob(raw_html, verbose, sort):
	""" set default encoding """
	reload(sys)
	sys.setdefaultencoding("utf-8")

	stats = PrettyTable()

	""" header """
	header = ["#", "Name", "Solves"]
	stats.field_names = header
	
	""" get problems table """
	probraw = raw_html.find_all("table", class_="problems")[0].find_all("tr")
	for row in probraw[1:]:
		tablerow = []
		if not verbose and row.has_attr("class") and row["class"][0] == "accepted-problem":
			continue
		cell = row.find_all("td")
		tablerow.append(str(cell[0].get_text(strip=True)))
		tablerow.append(str(cell[1].find("a").get_text(strip=True)))
		tablerow.append(int(str(cell[3].get_text(strip=True))[1:]))
		stats.add_row(tablerow)

	""" printing """
	stats.hrules = True
	stats.align["Name"] = "l"
	stats.align["Solves"] = "r"
	if sort == "solves":
		print stats.get_string(sortby="Solves", reversesort=True)
	elif sort == "index":
		print stats.get_string(sortby="#")
	else:
		print stats

def print_time(raw_html, verbose):
	print "work in progress"
