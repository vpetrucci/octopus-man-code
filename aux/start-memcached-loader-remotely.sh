#!/usr/bin/expect
eval spawn ssh -oStrictHostKeyChecking=no -oCheckHostIP=no vpetrucci@tucunare.cs.pitt.edu
#use correct prompt
set prompt ":|#|\\\$"

interact -o -nobuffer -re $prompt return
send "m4k1p1tt\r"

interact -o -nobuffer -re $prompt return
send "cd /afs/cs.pitt.edu/usr0/vpetrucci/disk2/memcached_client-octoman/ \r"

interact -o -nobuffer -re $prompt return
send "/afs/cs.pitt.edu/usr0/vpetrucci/disk2/memcached_client-octoman/loader -a ../memcached/twitter_dataset/twitter_dataset_30x -s ../memcached/memcached_client/servers.txt -g 0.8 -c 200 -w 8 -T 1 -r 36000 \r"

interact -o -nobuffer -re $prompt return
send "exit\r"
interact

