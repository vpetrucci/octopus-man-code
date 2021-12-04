#taskset -c 0 /afs/cs.pitt.edu/usr0/vpetrucci/disk2/nutch-test/search/bin/stop-all.sh

#sleep 3

taskset -c 0 /afs/cs.pitt.edu/usr0/vpetrucci/disk2/nutch-test/tomcat/bin/shutdown.sh 

taskset -c 0 /afs/cs.pitt.edu/usr0/vpetrucci/disk2/nutch-test/search/bin/hadoop-daemon.sh stop namenode
taskset -c 0 /afs/cs.pitt.edu/usr0/vpetrucci/disk2/nutch-test/search/bin/hadoop-daemon.sh stop datanode
taskset -c 0 /afs/cs.pitt.edu/usr0/vpetrucci/disk2/nutch-test/search/bin/hadoop-daemon.sh stop secondarynamenode

taskset -c 0 /afs/cs.pitt.edu/usr0/vpetrucci/disk2/nutch-test/search/bin/hadoop-daemon.sh stop jobtracker
taskset -c 0 /afs/cs.pitt.edu/usr0/vpetrucci/disk2/nutch-test/search/bin/hadoop-daemon.sh stop tasktracker
