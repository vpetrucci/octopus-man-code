#!/usr/bin/expect
eval spawn ssh -oStrictHostKeyChecking=no -oCheckHostIP=no vpetrucci@piabanha.cs.pitt.edu
#use correct prompt
set prompt ":|#|\\\$"

interact -o -nobuffer -re $prompt return
send "XXXX\r"

interact -o -nobuffer -re $prompt return
send "/afs/cs.pitt.edu/usr0/vpetrucci/wattsup -t ttyUSB0 watts > /tmp/power.txt &\r"

interact -o -nobuffer -re $prompt return
send "exit\r"
interact

