#!/bin/bash
             # map to small cores
      pid1=`ps ax | grep DarwinStreamingServer | awk '{print $1}'`
      for i in $pid1; do taskset -c -p $* $i; done
      # set also for children

     for i in $pid1; do
        child_i=`ls /proc/$i/task/`
        for j in $child_i; do taskset -c -p $* $j; done
     done

