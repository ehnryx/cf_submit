# cf-code-submit
Submit code to codeforces from the command line, and other stuff. <br />
<br />
In order to save the huge number of seconds needed to reach for the mouse during codeforces contests, I needed to be able to submit from the command line. There are many tools to do this for codeforces contests but I was unable to find an existing tool that allowed submissions to the codeforces gym for virtual contests, so I made this. <br />
After being able to submit from the command line, I noticed that I was wasting too much time staring at the standings on codeforces. Now I waste less time (hopefully) by staring at the standings in the terminal. <br />
Then I realized I would rather not navigate codeforces in my browser because looking for my mouse is a hassle, so now I can look at the number of solves for each problem in the terminal as well. <br />

# Uses
## Submissions
`con` or `gym` to set default contest or gym ID. Example: `cf con 844` or `cf gym 101482` <br />
`submit` to submit code. Will try to guess problem. Example: `cf submit` or `cf submit a.cpp` <br />
`--prob` or `-p` to specify problem. Example: `cf submit code.cpp -p 844a` <br />
`--watch` or `-w` to Watch the status of submission after submitting it. Example: `cf submit a.cpp -p 844a -w` <br />
`peek` to look at status of the last submission. Example: `cf peek` <br />
`watch` to watch the status of the last submission if `-w` was not used. Example: `cf watch` <br />
`login` to store login info (username and password), will prompt you to enter password. Example: `cf login` or `cf login henryx` <br />
`info` to show stored handle and contest id. Example: `cf info` <br />
Example: `cf submit code.cpp -p844a -w` <br />
## Standings and Problem Stats
`standings` or `st` to look at friends' standings. Example: `cf standings` <br />
`problems` or `pb` to look at the number of solves for each problem in a contest. Example: `cf problems` <br />
`--contest` or `-c` to specify the ID of the contest to look at. Example: `cf standings -c 844` <br />
`--verbose` or `-v` to Print standings with more info. Example: `cf standings -v` **option not available for `problems`** <br />
`--top` or `-t` to look top contestants instead of friends with `-t` or `--top`. Examples: `cf standings -t 20` <br />
If no number is given, `--top` defaults to printing the top 10. <br />
Examples: `cf standings -v -t7` or `cf standings -c844 -v -a` <br />

## Dependencies
robobrowser <br />
prettytable <br />
