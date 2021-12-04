#!/usr/bin/expect
eval spawn ssh -oStrictHostKeyChecking=no -oCheckHostIP=no vpetrucci@tucunare.cs.pitt.edu
#use correct prompt
set prompt ":|#|\\\$"

interact -o -nobuffer -re $prompt return
send "m4k1p1tt\r"

interact -o -nobuffer -re $prompt return
send "killall rtspclient.o; /afs/cs.pitt.edu/usr0/vpetrucci/disk2/streaming-release/faban-streaming/streaming/scripts/run-test.sh \r"

interact -o -nobuffer -re $prompt return
send "exit\r"
interact

