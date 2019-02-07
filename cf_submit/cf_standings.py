import re
from prettytable import PrettyTable

from .cf_colors import colors


def makeascii(s):
    return re.sub(r'[^\x00-\x7f]', r'?', s)


# print friends standings in specified contest
# parse html
# gym contest
def print_st(raw_html, verbose, top, sort):
    # get standings table
    global handledict
    mellon = raw_html.find_all("table", class_="standings")[0].find_all("tr")

    standings = PrettyTable()

    # get header
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
    # append sorter to header
    if sort is not None:
        header.append("sorter")
    standings.field_names = header

    id_start = 4
    if not verbose:
        id_start = 0
        for hcell in mellon[0].find_all("th"):
            hcellstr = str(hcell.get_text(strip=True))
            if hcellstr.find('A') != -1:
                break
            id_start += 1

    fields = dict()
    for i in range(0, len(header)):
        fields[header[i]] = i

    # find problemstart and solvecol
    problemstart = 0
    while header[problemstart].find("A") == -1:
        problemstart += 1
    solvecol = 0
    while header[solvecol] != "=":
        solvecol += 1

    # if sort, use dict
    if sort is not None:
        handledict = {}

    # fix top
    top = min(top + 1, len(mellon) - 1)
    # get rows
    rankrowlist = mellon[1:top]

    # iterate
    for ami in rankrowlist:
        virtual = True
        row = ami.find_all("td")
        tablerow = []
        # get place
        # this cell has problems
        rank = str(row[0].get_text(strip=True))
        if len(rank) == 0:
            virtual = False
        if verbose:
            if rank.find(')') != -1:
                rank = rank[rank.find('(') + 1:rank.find(')')]
            tablerow.append(rank)

        # get name
        party = str(row[1].get_text(strip=True))
        if verbose:
            team = []
            # check if virtual time colon
            virtualtime = None
            if party[-3] == ':':
                virtualtime = party[-5:]
                party = party[:-5]

            # check if there are still colons left if yes, split at last colon
            if party.count(':') > 0:
                # check for '#'
                tail = ""
                if party[-1] == '#':
                    tail = "#"
                    party = party[:-1]
                # split
                party = party.split(':')
                # get first part (team name)
                teamname = party[0]
                for partypart in party[1:-1]:
                    teamname += ":" + partypart
                if len(teamname + tail) > 24:
                    teamname = teamname[:20] + "..."
                teamname += tail + ":"
                team.append(teamname)
                # split rest of team members
                for member in party[-1].split(','):
                    team.append(member.strip())
            else:
                team.append(party)
            # append time if it exists"""
            if virtualtime is not None:
                team.append(virtualtime)
            # join party
            party = '\n'.join(team)
        else:
            if party[-3] == ':':
                party = party[:-5]
            if party.count(':') > 0:
                tail = ""
                if party[-1] == '#':
                    tail = "#"
                    party = party[:-1]
                # split
                party = party.split(':')
                teamname = party[0]
                for partypart in party[1:-1]:
                    teamname += ":" + partypart
                if len(teamname) > 32:
                    teamname = teamname[:32] + "..."
                teamname += tail
                party = teamname
        tablerow.append(makeascii(party))

        # get points or number of solves
        tablerow.append(int(str(row[2].get_text(strip=True))))
        # get penalty or hacks
        if verbose:
            tablerow.append(str(row[3].get_text(strip=True)))

        # get problem submissions
        for cell in row[id_start:]:
            problemres = str(cell.get_text(strip=True))
            if virtual and len(problemres) > 5:
                if verbose:
                    problemres = (problemres[:-5] + '\n' + problemres[-5:])
                else:
                    problemres = problemres[:-5]
            else:
                problemres = problemres.replace("-", "WA-")
            tablerow.append(problemres)

        # check sort
        if sort is not None:
            # add to dict
            # make party legible
            if party[0] == '*':
                party = party[1:]
            if party[-1] == '#':
                party = party[:-1]

            # check if party exists
            if party not in handledict:
                handledict[party] = tablerow
            else:
                # update
                for i in range(problemstart, len(header) - 1):
                    # update if empty or wa
                    if len(handledict[party][i]) == 0:
                        handledict[party][i] = tablerow[i]
                        # check if we should update solvecol
                        if len(tablerow[i]) != 0 and tablerow[i][0] == "+":
                            handledict[party][solvecol] += 1
                    elif handledict[party][i][0] != '+' and len(tablerow[i]) != 0:
                        totalwa = int(handledict[party][i].split(
                            '\n')[0].split('-')[1])
                        if tablerow[i].find('-') != -1:
                            # add wa
                            totalwa += int(tablerow[i].split('\n')
                                           [0].split('-')[1])
                            handledict[party][i] = "WA-" + str(totalwa)
                        else:
                            # add wa to correct submission
                            correct = tablerow[i].split('\n')[0][1:]
                            if len(correct) != 0:
                                totalwa += int(correct)
                            handledict[party][i] = "+" + str(totalwa)
                            # update solvecol
                            handledict[party][solvecol] += 1
        else:
            # NO sort, add to tablerow
            standings.add_row(tablerow)

    # standings properties
    if verbose:
        standings.hrules = True
        if "Penalty" in standings.align:
            standings.align["Penalty"] = "r"
    standings.align["Who"] = "l"
    standings.align["="] = "r"

    # print standings
    if sort is None:
        print(standings)

    elif sort == "solves":
        # add rowinfo to standings
        for key, rowinfo in handledict.items():
            # append the sorter
            sortvalue = rowinfo[fields["="]]
            if "Penalty" in fields:
                if len(rowinfo[fields["Penalty"]]) == 0:
                    sortvalue = 100000 * sortvalue - 99999
                else:
                    sortvalue = 100000 * sortvalue - \
                        int(rowinfo[fields["Penalty"]])
            rowinfo.append(sortvalue)
            standings.add_row(rowinfo)
        # print
        print(standings.get_string(
            sortby="sorter",
            reversesort=True,
            fields=header[:-1]
        ))

    elif sort == "index":
        print("sort == index : nothing here")

    else:
        print("this should not have happened. nothing here")

    # first check if countdown
    # boldstart = "\033[1m"
    # boldend = "\033[0;0m"
    countdown_timer = raw_html.find_all("span", class_="countdown")
    if len(countdown_timer) > 0:
        print("%sTIME LEFT: %s%s" %
              (colors.BOLD, str(countdown_timer[0].get_text(strip=True)), colors.ENDC))
