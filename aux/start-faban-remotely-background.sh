#!/usr/bin/expect
#spawn /bin/sh -c "ssh -oStrictHostKeyChecking=no -oCheckHostIP=vpetrucci no@tucunare.cs.pitt.edu"

eval spawn ssh -t -oStrictHostKeyChecking=no -oCheckHostIP=no vpetrucci@tucunare.cs.pitt.edu
#use correct prompt
set prompt ":|#|\\\$"

interact -o -nobuffer -re $prompt return
send "m4k1p1tt\r"

#interact -o -nobuffer -re $prompt return
#send "export JAVA_HOME=/usr/java/latest/ \r"

interact -o -nobuffer -re $prompt return
send "/afs/cs.pitt.edu/usr0/vpetrucci/disk2/search-release/faban/search/run-back.sh \r"
send "sleep 2 \r"

interact -o -nobuffer -re $prompt return
send "exit\r"
interact

