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

data=`date +%Y-%m-%d-%H%M`
path="/afs/cs.pitt.edu/usr0/vpetrucci/"

#apps=('calculix' 'lbm' 'hmmer' 'milc' 'libquantum' 'povray' 'tonto' 'gobmk' 'gromacs' 'namd' 'astar' 'cactusADM' 'soplex' 'leslie3d' 'zeusmp' 'sjeng')

#apps=('calculix' 'lbm' 'hmmer' 'milc' 'libquantum' 'povray' 'tonto' 'gobmk')

#apps=('calculix' 'astar' 'milc')

# todo: put none in the app list

#for bench in "${apps[@]}" ;
#do
    
#for policy in 'octopus_no_batch';

#up_thr="0.8"
#down_thr="0.4"

up_thrs=(0.8)
down_thrs=(0.3)

#up_thrs=(0.8)
#down_thrs=(0.1 0.2 0.3)

#up_thrs=(0.8)
#down_thrs=(0.2 0.3 0.4 0.5 0.6)

#filter="0.4"

#filter=(1.0 0.9 0.8 0.7 0.6 0.5 0.4 0.3 0.2)

filter=(1.0)

fil="1.0"

#set_factor="0"
#set_factor_list=(2 4 0)
set_factor_list=(0)

#for spiky in 'high' 'mid' 'low' 'smooth' ;
#for spiky in 'low' 'mid' 'high';
#do
for spiky in 'smooth' ;
do
    
#up_thrs=(0.8)
#down_thrs=(0.4)

#  echo ${u} ${d}

for set_factor in "${set_factor_list[@]}";
#for fil in "${filter[@]}";
do

# 100, 200, 400
#for deadline in '200' '100' '400' ;
#for deadline in '100' '150' '200' '250' ;
#for deadline in '100' '150' '200' ;
#for deadline in '125' '100' '150' ;
for deadline in '500' ;
do

# 5, 15, 30
#for interval in '15' '30' '5';
#for interval in '15' '5' '30'  ;
#for interval in '1' '2' '5' '10';
for interval in '10';
# '10';
#for interval in '5' '10' '15';
do

#for policy in 'reactive' 'static' 'static_batch' 'reactive_batch' 'reactive_batch_corun' ;
#for policy in 'reactive' 'reactive_batch' ;

#for policy in 'static_batch' 'reactive_batch' 'reactive_batch_corun' ;
#for policy in  'reactive_batch' 'reactive_batch_corun' ;
#for policy in 'reactive_batch_corun' 'static_batch' 'reactive_batch' 'reactive' 'static' ;
#for policy in 'static_batch' 'reactive_batch' 'reactive_batch_corun' ;
#for policy in  'static_batch' 'reactive_batch' ;
#'reactive' 'static'
#for policy in 'reactive' 'static';
#for policy in 'reactive_swap' 'static' 'static_wimpy';
#for policy in 'pidcontrol' 'reactive';
#for policy in 'reactive90adapt';
#for policy in 'reactive90adapt' 'static' 'static_wimpy';
#for policy in 'pidcontrol' 'reactive90adapt' 'static' 'static_wimpy';
for policy in 'reactive90adapt' 'static';
#for policy in 'reactive90adapt' 'static';
#for policy in 'pidcontrol';
#for policy in 'pidcontrol';
#for policy in 'qospred' 'pidcontrol' 'pidqoscontrol' 'reactive' 'static';
#for policy in 'reactive_swap' 'static' 'static_wimpy' ;
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


    if [ $spiky = 'smooth' ];
    then

         c=75
          val='/afs/cs.pitt.edu/usr0/vpetrucci/load-google-2-days.txt'

#            c=76
 #           val='/afs/cs.pitt.edu/usr0/vpetrucci/load-google-1-day.txt'

        #val='/afs/cs.pitt.edu/usr0/vpetrucci/load-google-30s-subset.txt'
        #val='/afs/cs.pitt.edu/usr0/vpetrucci/load-short.txt'
# val='/afs/cs.pitt.edu/usr0/vpetrucci/load-file-google-subset2.txt'

# sed -i  -e 's#\(<fa:variableLoadFile>\).*\(</fa:variableLoadFile>\)#\1'$val'\2#g' /afs/cs.pitt.edu/usr0/vpetrucci/deploy/run.xml
        
  # sed -i  -e 's#\(<fa:steadyState>\)[0-9]*\(</fa:steadyState>\)#\1'1440'\2#g' /afs/cs.pitt.edu/usr0/vpetrucci/deploy/run.xml

         sed -i  -e 's#\(<fa:steadyState>\)[0-9]*\(</fa:steadyState>\)#\1'2880'\2#g' /afs/cs.pitt.edu/usr0/vpetrucci/deploy/run.xml

         sed -i  -e 's#\(<fa:scale>\)[0-9]*\(</fa:scale>\)#\1'$c'\2#g' /afs/cs.pitt.edu/usr0/vpetrucci/deploy/run.xml
         sed -i  -e 's#\(<fa:variableLoadFile>\).*\(</fa:variableLoadFile>\)#\1'$val'\2#g' /afs/cs.pitt.edu/usr0/vpetrucci/deploy/run.xml

    else
      val='/afs/cs.pitt.edu/usr0/vpetrucci/wc98-'$spiky'-spiky.txt'
        sed -i  -e 's#\(<fa:variableLoadFile>\).*\(</fa:variableLoadFile>\)#\1'$val'\2#g' /afs/cs.pitt.edu/usr0/vpetrucci/deploy/run.xml
   
      sed -i  -e 's#\(<fa:steadyState>\)[0-9]*\(</fa:steadyState>\)#\1'720'\2#g' /afs/cs.pitt.edu/usr0/vpetrucci/deploy/run.xml

    fi

#    val='/afs/cs.pitt.edu/usr0/vpetrucci/toy-load.txt'
#    val='/afs/cs.pitt.edu/usr0/vpetrucci/toy-load-up-down.txt'    


#    sed -i  -e 's#\(<fa:steadyState>\)[0-9]*\(</fa:steadyState>\)#\1'540'\2#g' /afs/cs.pitt.edu/usr0/vpetrucci/deploy/run.xml
#    sed -i  -e 's#\(<fa:steadyState>\)[0-9]*\(</fa:steadyState>\)#\1'600'\2#g' /afs/cs.pitt.edu/usr0/vpetrucci/deploy/run.xml    

    # toy workload for debugging 
#    val='/afs/cs.pitt.edu/usr0/vpetrucci/toy-load-up-down2.txt'      
#    sed -i  -e 's#\(<fa:variableLoadFile>\).*\(</fa:variableLoadFile>\)#\1'$val'\2#g' /afs/cs.pitt.edu/usr0/vpetrucci/deploy/run.xml
#    sed -i  -e 's#\(<fa:steadyState>\)[0-9]*\(</fa:steadyState>\)#\1'1080'\2#g' /afs/cs.pitt.edu/usr0/vpetrucci/deploy/run.xml        
#    sed -i  -e 's#\(<fa:scale>\)[0-9]*\(</fa:scale>\)#\1'78'\2#g' /afs/cs.pitt.edu/usr0/vpetrucci/deploy/run.xml
    # end of toy config  


    #sh /afs/cs.pitt.edu/usr0/vpetrucci/move-tomcat-jobs.sh 0
        
    sh /afs/cs.pitt.edu/usr0/vpetrucci/move-memcached.sh 4,5
    sh /afs/cs.pitt.edu/usr0/vpetrucci/move-cassandra.sh 4,5

    sh /afs/cs.pitt.edu/usr0/vpetrucci/move-tomcat.sh 2,3
    
    full_path=$path/disk2/hetero-websearch-${data}/${policy}-${interval}-${deadline}-${bench}-${up}-${down}-${fil}-${spiky}-${set_factor}
    mkdir -p $full_path

    rm -rf /afs/cs.pitt.edu/usr0/vpetrucci/faban-output/*

    cur_date=`date +%Y-%m-%d`
    echo -n > /ramcache/logs/localhost_access_log.$cur_date.txt

    # start power monitor
    sleep 20 && /afs/cs.pitt.edu/usr0/vpetrucci/start-power-mon.sh


    # best down parameter
#    if [ $policy = 'reactive' ]; 
#    then
#        down="0.1"
#    fi    

    # start hetero mapper
    echo -n 1 > /ramcache/mapper_running
#    sleep 20 && taskset -c 3 python /afs/cs.pitt.edu/usr0/vpetrucci/hetero-mapper3-adapt-deadzone.py $policy $interval $deadline $up $down $fil &
    sleep 20 && taskset -c 5 python /afs/cs.pitt.edu/usr0/vpetrucci/octopus-man-control.py $policy $interval $deadline $up $down $fil tomcat $set_factor &

    # start workload generator
    #taskset -c 3 /afs/cs.pitt.edu/usr0/vpetrucci/start-faban-ramp-remotely.sh
    taskset -c 5 /afs/cs.pitt.edu/usr0/vpetrucci/start-faban-remotely.sh 

    # finalize mapper
    echo -n 0 > /ramcache/mapper_running

    # top power monitor
   /afs/cs.pitt.edu/usr0/vpetrucci/stop-power-mon.sh

    sleep 10
        
#    sh /afs/cs.pitt.edu/usr0/vpetrucci/kill-experiment.sh

   sync
   mv  /afs/cs.pitt.edu/usr0/vpetrucci/power.txt $full_path

    mv /ramcache/hetero-mapper.txt $full_path
    mv /ramcache/perf-monitor.txt $full_path
    cp -r -p /afs/cs.pitt.edu/usr0/vpetrucci/faban-output/* $full_path
    cp /ramcache/logs/localhost_access_log.$cur_date.txt $full_path

 #   cp /ramcache/running_times $full_path

    sleep 20
    
  #  ps1=`ps -P ax | grep tail | egrep 'S[^+]' | cut -f1 -d" "`
  #  kill $ps1

done
done
done
done
done
done
done

