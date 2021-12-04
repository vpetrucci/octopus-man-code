#!/usr/bin/expect
set arg1 [lindex $argv 0]
eval spawn ssh -oStrictHostKeyChecking=no -oCheckHostIP=no vpetrucci@tucunare.cs.pitt.edu
#use correct prompt
set prompt ":|#|\\\$"

interact -o -nobuffer -re $prompt return
send "m4k1p1tt\r"

interact -o -nobuffer -re $prompt return
send "export JAVA_HOME=/usr/lib/jvm/java-1.6.0/ \r"

interact -o -nobuffer -re $prompt return
send "/afs/cs.pitt.edu/usr0/vpetrucci/cassandra-ramp-up-down.sh $arg1 \r"


interact -o -nobuffer -re $prompt return
send "exit\r"
interact

