#!/bin/bash

java -cp /afs/cs.pitt.edu/usr0/vpetrucci/disk2/YCSB/build/ycsb.jar:/afs/cs.pitt.edu/usr0/vpetrucci/disk2/YCSB/db/cassandra-0.7/lib/* com.yahoo.ycsb.Client -t -s -db com.yahoo.ycsb.db.CassandraClient7 -P /afs/cs.pitt.edu/usr0/vpetrucci/disk2/YCSB/workloads/workloadx -P /afs/cs.pitt.edu/usr0/vpetrucci/disk2/YCSB/settings.dat 
