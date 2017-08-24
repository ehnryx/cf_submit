# cf-code-submit
submit code to codeforces from command line <br />
In order to save the huge number of seconds needed to reach for the mouse during a codeforces virtual contest, I needed to be able to submit from the command line. There are many tools to do this for codeforces contests but I was unable to find an existing tool that allowed submissions to the codeforces gym, so I made my own. <br />

## Uses
Set contest or gym ID. Example: `cf con 844` or `cf gym 101482` <br />
Submit code to a problem, will guess problem. Example: `cf submit` or `cf submit a.cpp` <br />
Specify a problem with `-p` or `--prob`. Example: `cf submit code.cpp -p 844a` <br />
Watch the status of submission with `-w` or `--watch`. Example: `cf submit a.cpp -p 844a -w` <br />
Look at status of the last submission. Example: `cf peek` <br />
Watch the status of the last submission. Example: `cf watch` <br />
Store login info (username and password), will prompt you to enter password. Example: `cf login` or `cf login henryx` <br />

## Dependencies
robobrowser <br />
