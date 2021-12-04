#!/usr/bin/expect
eval spawn ssh -oStrictHostKeyChecking=no -oCheckHostIP=no vpetrucci@tucunare.cs.pitt.edu
#use correct prompt
set prompt ":|#|\\\$"

interact -o -nobuffer -re $prompt return
send "m4k1p1tt\r"

interact -o -nobuffer -re $prompt return
send "export JAVA_HOME=/usr/lib/jvm/java-1.6.0/ \r"

interact -o -nobuffer -re $prompt return
#send "/afs/cs.pitt.edu/usr0/vpetrucci/faban-ramp-up-down.sh \r"
send "/afs/cs.pitt.edu/usr0/vpetrucci/faban-ramp-up-down.sh \r"


interact -o -nobuffer -re $prompt return
send "exit\r"
interact

