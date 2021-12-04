#!/bin/bash

# run batch apps


#python /afs/cs.pitt.edu/usr0/vpetrucci/run-apps2.py lbm &
#python /afs/cs.pitt.edu/usr0/vpetrucci/run-apps2.py lbm &

#python /afs/cs.pitt.edu/usr0/vpetrucci/run-apps2.py calculix  & pid1=$!
#python /afs/cs.pitt.edu/usr0/vpetrucci/run-apps2-copy.py calculix  & pid2=$!

#python /afs/cs.pitt.edu/usr0/vpetrucci/run-batch-jobs.py &

# calculix
# astar
# milc

path="/afs/cs.pitt.edu/usr0/vpetrucci/"
data=`date +%Y-%m-%d-%H%M`

#apps=('calculix' 'lbm' 'hmmer' 'milc' 'libquantum' 'povray' 'tonto' 'gobmk' 'gromacs' 'namd' 'astar' 'cactusADM' 'soplex' 'leslie3d' 'zeusmp' 'sjeng')

#apps=('calculix' 'lbm' 'hmmer' 'milc' 'libquantum' 'povray' 'tonto' 'gobmk')

#apps=('calculix' 'astar' 'milc')

# todo: put none in the app list

#for bench in "${apps[@]}" ;
#do
    
#for policy in 'octopus_no_batch';

#up_thr="0.7"
#down_thr="0.4"

#up_thrs=(0.8)
#down_thrs=(0.1 0.2 0.3 0.4)

#filter=(1.0 0.9 0.8 0.7 0.6 0.5 0.4 0.3 0.2)

filter=(1.0)

#set_factor="0"

up_thrs=(0.8)
down_thrs=(0.3)

#up_thrs=(0.8)
#down_thrs=(0.1 0.2 0.3 0.4)

#set_factor_list=(2 4 0)
set_factor_list=(0)

fil="1.0"

rm /ramcache/loader-memcached.txt

for set_factor in "${set_factor_list[@]}";
#for fil in "${filter[@]}";
do

for spiky in 'smooth' ;    
#for spiky in 'smooth' ;
do
    
#  echo ${u} ${d}

# 100, 200, 400
#for deadline in '200' '100' '400' ;
#for deadline in '100' '150' '200' '250' ;
#for deadline in '100' '150' '200' ;
#for deadline in '125' '100' '150' ;
for deadline in '1' ;
do

# 5, 15, 30
#for interval in '15' '30' '5';
#for interval in '15' '5' '30'  ;
#for interval in '1' '2' '5' '10';
#for interval in '1' '5' '10';
for interval in '5';
do

#for policy in 'reactive' 'static' 'static_batch' 'reactive_batch' 'reactive_batch_corun' ;
#for policy in 'reactive' 'reactive_batch' ;

#for policy in 'static_batch' 'reactive_batch' 'reactive_batch_corun' ;
#for policy in  'reactive_batch' 'reactive_batch_corun' ;
#for policy in 'reactive_batch_corun' 'static_batch' 'reactive_batch' 'reactive' 'static' ;
#for policy in 'static_batch' 'reactive_batch' 'reactive_batch_corun' ;
#for policy in  'static_batch' 'reactive_batch' ;
#'reactive' 'static'
#for policy in 'static' 'static_wimpy';
#for policy in 'static_wimpy';
#'pidqoscontrol95'
#for policy in 'reactive95adapt' 'static' 'static_wimpy';
for policy in 'pidcontrol95';
#for policy in 'reactive95';
#for policy in 'reactive_batch' 'static' 'static_wimpy';
#for policy in 'static' 'static_wimpy';
#for policy in 'static_wimpy' 'reactive_batch' 'static';
do
    
for up in "${up_thrs[@]}"
do
for down in "${down_thrs[@]}"
do

#    if [ $policy = 'static_batch' ] || [ $policy = 'reactive_batch' ] ; 
#    then
#        python /afs/cs.pitt.edu/usr0/vpetrucci/run-apps2-copy.py $bench 0 & 
#        python /afs/cs.pitt.edu/usr0/vpetrucci/run-apps2-copy.py $bench 1 &       
#    fi

#    if [ $policy = 'reactive_batch_corun' ]; 
#    then
#        python /afs/cs.pitt.edu/usr0/vpetrucci/run-apps2-copy.py $bench 0 & 
#        python /afs/cs.pitt.edu/usr0/vpetrucci/run-apps2-copy.py $bench 1 & 
#        python /afs/cs.pitt.edu/usr0/vpetrucci/run-apps2-copy.py $bench 2 &       
#    fi
    sh /afs/cs.pitt.edu/usr0/vpetrucci/move-tomcat.sh 4,5
    sh /afs/cs.pitt.edu/usr0/vpetrucci/move-cassandra.sh 4,5

    sh /afs/cs.pitt.edu/usr0/vpetrucci/move-memcached.sh 2,3

    full_path=$path/disk2/hetero-memcached-${data}/${policy}-${interval}-${deadline}-${bench}-${up}-${down}-${fil}-${spiky}-${set_factor}
    mkdir -p $full_path    
    
#    if [ $spiky = 'smooth' ];
 #   then
  #      cp /afs/cs.pitt.edu/usr0/vpetrucci/disk2/memcached_client-octoman/load-smooth.cfg /afs/cs.pitt.edu/usr0/vpetrucci/disk2/memcached_client-octoman/load.cfg
  #
   # else
    #    cp /afs/cs.pitt.edu/usr0/vpetrucci/disk2/memcached_client-octoman/load-bursty-$spiky.cfg /afs/cs.pitt.edu/usr0/vpetrucci/disk2/memcached_client-octoman/load.cfg
    #fi    
        
 #   rm -rf /afs/cs.pitt.edu/usr0/vpetrucci/faban-output/*

 #   cur_date=`date +%Y-%m-%d`
 #   echo -n > /ramcache/logs/localhost_access_log.$cur_date.txt

    # start power monitor
    sleep 20 && /afs/cs.pitt.edu/usr0/vpetrucci/start-power-mon.sh

#    if [ $policy = 'reactive95' ]; 
#    then
#        down="0.1"
#    fi    

    # start hetero mapper
    echo -n 1 > /ramcache/mapper_running
    sleep 20 && taskset -c 5 python /afs/cs.pitt.edu/usr0/vpetrucci/octopus-man-control.py $policy $interval $deadline $up $down $fil memcached $set_factor &

    # start workload generator
    #taskset -c 3 /afs/cs.pitt.edu/usr0/vpetrucci/start-faban-ramp-remotely.sh
 #   taskset -c 3 /afs/cs.pitt.edu/usr0/vpetrucci/start-faban-remotely.sh
    cd /afs/cs.pitt.edu/usr0/vpetrucci/disk2/memcached_client-octoman/
    
    echo 'starting memcached loader..'
  #  taskset -c 4,5 /afs/cs.pitt.edu/usr0/vpetrucci/disk2/memcached_client-octoman/loader -a $path/disk2/memcached/twitter_dataset/twitter_dataset_30x -s $path/disk2/memcached/servers.txt -g 0.8 -c 200 -w 8 -T 1 -r 41333 > /ramcache/loader-memcached.txt

    taskset -c 5 unbuffer /afs/cs.pitt.edu/usr0/vpetrucci/start-memcached-loader-remotely.sh > /ramcache/loader-memcached.txt   


 # top power monitor
    /afs/cs.pitt.edu/usr0/vpetrucci/stop-power-mon.sh
    
    # finalize mapper
    echo -n 0 > /ramcache/mapper_running

    sleep 5
        
   # sh /afs/cs.pitt.edu/usr0/vpetrucci/kill-experiment.sh

  # sync
   mv  /afs/cs.pitt.edu/usr0/vpetrucci/power.txt $full_path

   mv /ramcache/loader-memcached.txt $full_path
  
    mv /ramcache/hetero-mapper.txt $full_path
   # mv /ramcache/perf-monitor.txt $full_path
  #  cp -r -p /afs/cs.pitt.edu/usr0/vpetrucci/faban-output/* $full_path
  #  cp /ramcache/logs/localhost_access_log.$cur_date.txt $full_path

 #   cp /ramcache/running_times $full_path

 #   sync

    sleep 25
    
  #  ps1=`ps -P ax | grep tail | egrep 'S[^+]' | cut -f1 -d" "`
  #  kill $ps1

done
done
done
done
done
done
done

kill $pid1
kill $pid2

ps1=`ps -P ax | grep run-apps2 | egrep 'S[^+]' | cut -f1 -d" "`
echo $ps1
kill $ps1

ps1=`ps -P ax | grep run-apps2 | egrep 'S[^+]' | cut -f2 -d" "`
echo $ps1
kill $ps1

ps3=`ps -P ax | grep cpu2006 | egrep 'R[^+]' | cut -f1 -d" "`
echo $ps3
kill -9 $ps3

ps3=`ps -P ax | grep cpu2006 | egrep 'R[^+]' | cut -f2 -d" "`
echo $ps3
kill -9 $ps3

sh /afs/cs.pitt.edu/usr0/vpetrucci/kill-experiment.sh
  
  ps3=`ps -P ax | grep cpu2006 | egrep 'R[^+]' | cut -f1 -d" "`
  echo $ps3
  kill $ps3

  ps3=`ps -P ax | grep cpu2006 | egrep 'R[^+]' | cut -f2 -d" "`
  echo $ps3
  kill $ps3
  
  ps3=`ps -P ax | grep cpu2006 | egrep 'R[^+]' | cut -f3 -d" "`
  echo $ps3
  kill $ps3 

  ps3=`ps -P ax | grep cpu2006 | egrep 'R[^+]' | cut -f4 -d" "`
  echo $ps3
  kill $ps3 
