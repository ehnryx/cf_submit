# cf-code-submit
Submit code to codeforces from the command line, and other stuff (display solves for each problem, display standings). <br />

In order to save the huge number of seconds needed to reach for the mouse during codeforces contests, I needed to be able to submit from the command line. There are many tools to do this for codeforces contests but I was unable to find an existing tool that allowed submissions to the codeforces gym for virtual contests, so I made this.

After being able to submit from the command line, I noticed that I was wasting too much time staring at the standings on codeforces. Now I waste less time (hopefully) by staring at the standings in the terminal.

Then I realized I would rather not navigate codeforces in my browser because looking for my mouse is a hassle, so now I can look at the number of solves for each problem in the terminal as well.

# NEW
Add autocomplete while writing the command (double TAB).

# Setup (Linux)
- Install from pip. `sudo pip install cf_submit`

# Uses
## Submissions
- `con` or `gym` to set default contest or gym ID. Example: `cf con 844` or `cf gym 101482`
- `gcon` to set default group and contest ID. Example: `cf gcon dyEemqw7jN 233642`
- `ext` to set default file extension. Will be used when no file extension is given. (`cf submit a`)
- `submit` to submit code. Will try to guess problem. Batch submit allowed. Example: `cf submit` or `cf submit a.cpp`
- `--prob` or `-p` to specify problem. Example: `cf submit code.cpp -p 844a`
- `--watch` or `-w` to Watch the status of submission after submitting it. Example: `cf submit a.cpp -p 844a -w`
- `peek` to look at status of the last submission. Example: `cf peek`
- `watch` to watch the status of the last submission if `-w` was not used. Example: `cf watch`
- `login` to store login info (username and password), will prompt you to enter password. Example: `cf login` or `cf login <your handle>`
- `info` to show stored handle and contest id. Example: `cf info`
- `time` to show time left in contest
- `open` to open the selected problem in the browser

Examples: `cf submit code.cpp -p844a -w` <br />

## Parse problem samples
- `parse` to import selected problem samples data

Examples: `cf parse -p 1108a` or `cf parse -p a` <br />

## Test solution
- `test` to test the selected source code with the imported tests data

Examples: `cf test main.cpp`, you should specify the version for python (use `-l py2|py3`) <br />

## Print Standings
- `standings` or `st` to look at friends' standings. Example: `cf standings`
- `--contest` or `-c` to specify the ID of the contest to look at. Example: `cf standings -c 844`
- `--group` to specify the ID of the group to look at. Example: `cf standings --group dyEemqw7jN`
- `--verbose` or `-v` to print standings with more info. Example: `cf standings -v`
- `--top` or `-t` to look top contestants. Defaults to top 50 if `-t` is not included, top 10 if `--top` is included but no number is given. Example: `cf standings -t 20`
- `--all` or `-a` to look at all contestants instead of only friends. Example: `cf standings --all`
- `--sort` or `-s` to merge the solves of different rows belonging to the same handle. Will not merge two correct submissions on different rows. Example: `cf standings -s`

Examples: `cf st -v -t7` or `cf standings -c844 -v -a` <br />

## Print Problem Stats
- `problems` or `pb` to look at the number of solves for each unsolved problem in a contest. Example: `cf problems`
- `--contest` or `-c` to specify the ID of the contest. Example: `cf problems -c 844`
- `--group` to specify the ID of the group. Example: `cf problems --group dyEemqw7jN`
- `--verbose` or `-v` to show solved problems as well. Example: `cf problems -v`
- `--sort` or `-s` to sort problems by: number of `solves`, or `index` (`id`). Default sort is by number of solves (you do not need to use `--sort`). Example: `cf problems -s id`

Exmaples: `cf pb -v -s id` or `cf problems -c100187 -v` <br />

## Hack
- `hack` to begin the hack proccess. 
- `--prob` or `-p` to specify problem. 
- `--number` or `-n` to specify the number of tests to try. 

Exmaples: `cf hack generator.cpp checker.cpp bruteforce.cpp --prob a` <br/>

## Note
This script uses python3
