#!/usr/bin/expect

#set arg1 [lindex $argv 0]

eval spawn ssh -oStrictHostKeyChecking=no -oCheckHostIP=no vpetrucci@tucunare.cs.pitt.edu
#use correct prompt
set prompt ":|#|\\\$"

interact -o -nobuffer -re $prompt return
send "m4k1p1tt\r"

interact -o -nobuffer -re $prompt return
#send "unbuffer /afs/cs.pitt.edu/usr0/vpetrucci/run-cassandra.sh x 2> /afs/cs.pitt.edu/usr0/vpetrucci/cassandra.out \r"
send "java -cp /afs/cs.pitt.edu/usr0/vpetrucci/disk2/YCSB/build/ycsb.jar:/afs/cs.pitt.edu/usr0/vpetrucci/disk2/YCSB/db/cassandra-0.7/lib/* com.yahoo.ycsb.Client -t -s -db com.yahoo.ycsb.db.CassandraClient7 -P /afs/cs.pitt.edu/usr0/vpetrucci/disk2/YCSB/workloads/workloadx -P /afs/cs.pitt.edu/usr0/vpetrucci/disk2/YCSB/settings.dat  \r"

interact -o -nobuffer -re $prompt return
send "exit\r"
interact

