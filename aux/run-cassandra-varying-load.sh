#!/bin/bash


#for c in 11573 12693 12413 12880 12320 11853 10266 9333 8026 8960 9240 9333 10266 11573 11760 12880 13253 14000 13066 13440 13346 12880 11573 11200;
for c in 4800 5600 6400 8800 12800 12800 12800 12800 13120 13280 13280 12800 11200 8000 4800 3200 1600 800 480 800 1600 3200 4800 8800 11200 12000 12800 13120 13280 13600 13440 13440 13600 13600 13600 13280 11200 9600 6400 4800 3200 1600 800 800 1600 4800 8000 9600;
do

     op_count=`echo "$c * 60" | bc`

     sed -i  -e 's#\(target=\)[0-9]*$#\1'$c'#g' /afs/cs.pitt.edu/usr0/vpetrucci/disk2/YCSB/settings.dat
     sed -i  -e 's#\(operationcount=\)[0-9]*$#\1'$op_count'#g' /afs/cs.pitt.edu/usr0/vpetrucci/disk2/YCSB/settings.dat
     
     java -cp /afs/cs.pitt.edu/usr0/vpetrucci/disk2/YCSB/build/ycsb.jar:/afs/cs.pitt.edu/usr0/vpetrucci/disk2/YCSB/db/cassandra-0.7/lib/* com.yahoo.ycsb.Client -t -s -db com.yahoo.ycsb.db.CassandraClient7 -P /afs/cs.pitt.edu/usr0/vpetrucci/disk2/YCSB/workloads/workloadx -P /afs/cs.pitt.edu/usr0/vpetrucci/disk2/YCSB/settings.dat  & pid=$!

     wait $pid

done
