# cf-code-submit
Submit code to codeforces from the command line, and other stuff. <br />
<br />
In order to save the huge number of seconds needed to reach for the mouse during codeforces contests, I needed to be able to submit from the command line. There are many tools to do this for codeforces contests but I was unable to find an existing tool that allowed submissions to the codeforces gym for virtual contests, so I made this. <br />
After being able to submit from the command line, I noticed that I was wasting too much time staring at the standings on codeforces. Now I waste less time (hopefully) by staring at the standings in the terminal. <br />
Then I realized I would rather not navigate codeforces in my browser because looking for my mouse is a hassle, so now I can look at the number of solves for each problem in the terminal as well. <br />

# Uses
## Submissions
Set default contest or gym ID. Example: `cf con 844` or `cf gym 101482` <br />
Submit code to a problem, will guess problem. Example: `cf submit` or `cf submit a.cpp` <br />
Specify a problem with `-p` or `--prob`. Example: `cf submit code.cpp -p 844a` <br />
Watch the status of submission after submitting it with `-w` or `--watch`. Example: `cf submit a.cpp -p 844a -w` <br />
Look at status of the last submission. Example: `cf peek` <br />
Watch the status of the last submission. Example: `cf watch` <br />
Store login info (username and password), will prompt you to enter password. Example: `cf login` or `cf login henryx` <br />
Example: `cf submit code.cpp -p844a -w` <br />
## Standings and Problem Stats
Look at friends' standings of defalut contest. Example: `cf standings` <br />
Look at the number of solves for each problem in a contest. Example: `cf problems` <br />
Look at a different contest by specifying the ID with `-c` or `--contest`. Example: `cf standings -c 844` <br />
Print standings or problems with more info with `-v` or `--verbose`. Example: `cf standings -v` <br />
Look at the standings of top contestants instead of friends with `-t` or `--top`. Examples: `cf standings -t 20` <br />
If no number is given, `--top` defaults to printing the top 10. <br />
Look at actual (not virtual contest) standings or stats with `--casual` or `a`. ** work in progress ** <br />
Examples: `cf standings -v -t7` or `cf standings -c844 -v -a` <br />

## Dependencies
robobrowser <br />
prettytable <br />
