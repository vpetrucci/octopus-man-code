#!/bin/bash
             # map to small cores
      pid1=`ps ax | grep apache-cassandra | awk '{print $1}'`
      for i in $pid1; do taskset -c -p $* $i; done
      # set also for children

     for i in $pid1; do
        child_i=`ls /proc/$i/task/`
        for j in $child_i; do taskset -c -p $* $j; done
     done

#     if [ $* == "0" ];
#     then
#        #echo '1 small'
#        sudo bash -c "echo 1 > /proc/irq/1270/smp_affinity"
#     elif [ $* == "0,1" ];
#     then
#       #echo '2 small'
#        sudo bash -c "echo 3 > /proc/irq/1270/smp_affinity"     
#     elif [ $* == "2" ];
#     then
#        #echo '1 big'
#        sudo bash -c "echo 4 > /proc/irq/1270/smp_affinity"     
#     elif [ $* == "2,3" ];
#     then
#           #echo '2 big'
#        sudo bash -c "echo c > /proc/irq/1270/smp_affinity"     
#     fi
