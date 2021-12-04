export JAVA_HOME=/usr/lib/jvm/java-6-sun/


#taskset -c 0 /afs/cs.pitt.edu/usr0/vpetrucci/disk2/nutch-test/search/bin/start-all.sh 




sleep 3

taskset -c 0 /afs/cs.pitt.edu/usr0/vpetrucci/disk2/nutch-test/search/bin/hadoop-daemon.sh start namenode
taskset -c 0 /afs/cs.pitt.edu/usr0/vpetrucci/disk2/nutch-test/search/bin/hadoop-daemon.sh start datanode
taskset -c 0 /afs/cs.pitt.edu/usr0/vpetrucci/disk2/nutch-test/search/bin/hadoop-daemon.sh start secondarynamenode

sleep 2

taskset -c 0 /afs/cs.pitt.edu/usr0/vpetrucci/disk2/nutch-test/search/bin/hadoop-daemon.sh start jobtracker

taskset -c 0 /afs/cs.pitt.edu/usr0/vpetrucci/disk2/nutch-test/search/bin/hadoop-daemon.sh start tasktracker

sleep 2

#taskset -c 0 /afs/cs.pitt.edu/usr0/vpetrucci/disk2/nutch-test/search/bin/hadoop-daemon.sh stop jobtracker
#sleep 5

#taskset -c 0 /afs/cs.pitt.edu/usr0/vpetrucci/disk2/nutch-test/search/bin/hadoop-daemon.sh start jobtracker
sleep 3

taskset -c 0 /afs/cs.pitt.edu/usr0/vpetrucci/disk2/nutch-test/tomcat/bin/startup.sh

sleep 2

for i in `ps ax | grep bin/java | cut -f1 -d" " | head -n 5`; do taskset -c -p 0,1,2,4 $i; done
for i in `ps ax | grep bin/java | cut -f2 -d" " | head -n 5`; do taskset -c -p 0,1,2,4 $i; done
