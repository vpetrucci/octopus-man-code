#
#     Vinicius Petrucci, UCSD 
#     2013
#
#

#apps=('canneal')

path="/afs/cs.pitt.edu/usr0/vpetrucci/"
data=`date +%Y-%m-%d-%H%M`
full_path=$path/disk2/websearch-quickia/${data}
mkdir -p $full_path

cd /ramcache/

a="search"

for c in 25 50 100 150 200 250;
#for c in 250;
do
 for interval in 200 500 1000 2000;
# for type in 'big';
 do

#  echo Starting power monitor...
#  /afs/cs.pitt.edu/usr0/vpetrucci/start-power-mon.sh
#  sleep 2

  # change num of clients
  sed -i  -e 's#\(<fa:scale>\)[0-9]*\(</fa:scale>\)#\1'$c'\2#g' /afs/cs.pitt.edu/usr0/vpetrucci/deploy/run.xml
  sync
  
  echo Starting performance monitor...
 # if [ $type == big ];
 # then
#    taskset -c 5 /afs/cs.pitt.edu/usr0/vpetrucci/likwid-3.0/likwid-perfctr -o perf-big-$a.txt -t 1s -c 3 -g INSTR_RETIRED_ANY:FIXC0,L2_LINES_IN_THIS_CORE_ALL:PMC0,BUS_TRANS_MEM_THIS_CORE_THIS_A:PMC1 &
    #taskset -c 5 /afs/cs.pitt.edu/usr0/vpetrucci/likwid-3.0/likwid-perfctr -o perf-big-$a.txt -t 1s -c 3 -g INSTR_RETIRED_ANY:FIXC0,L1D_REPL:PMC0,L2_LINES_IN_THIS_CORE_ALL:PMC1 &
    sleep 5 && taskset -c 5 /afs/cs.pitt.edu/usr0/vpetrucci/likwid-3.0/likwid-perfctr -o perf-$a.txt -t 50ms -c 0,1,2,4 -g INSTR_RETIRED_ANY:FIXC0,L2_RQSTS_SELF_MESI:PMC0,L2_LINES_IN_THIS_CORE_ALL:PMC1 &
    #taskset -c 5 /afs/cs.pitt.edu/usr0/vpetrucci/likwid-3.0/likwid-perfctr -o perf-big-$a.txt -t 1s -c 4 -g INSTR_RETIRED_ANY:FIXC0,RESOURCE_STALLS_ANY:PMC0,RAT_STALLS_ANY:PMC1 &
 # else
#    taskset -c 5 /afs/cs.pitt.edu/usr0/vpetrucci/likwid-3.0/likwid-perfctr -o perf-small-$a.txt -t 1s -c 0 -g INSTR_RETIRED_ANY:FIXC0,L1D_REPL:PMC0,L2_LINES_IN_THIS_CORE_ALL:PMC1 &
 #   sleep 5 && taskset -c 5 /afs/cs.pitt.edu/usr0/vpetrucci/likwid-3.0/likwid-perfctr -o perf-small-$a.txt -t 1s -c 0,1,2,4 -g INSTR_RETIRED_ANY:FIXC0,L2_RQSTS_SELF_MESI:PMC0,L2_LINES_IN_THIS_CORE_ALL:PMC1 &

 # fi
  #sleep 1
  
#  if [ $type == big ];
#  then
#      echo "Running websearch on big cores..."
#      sh /afs/cs.pitt.edu/usr0/vpetrucci/all-java-to-big-cores.sh             
#  else
#      echo "Running websearch on small cores..."
#      sh /afs/cs.pitt.edu/usr0/vpetrucci/all-java-to-small-cores.sh             
#  fi

  taskset -c 3 /afs/cs.pitt.edu/usr0/vpetrucci/java-migrator $interval &
  
  taskset -c 3 /afs/cs.pitt.edu/usr0/vpetrucci/start-faban-remotely.sh

  echo Killing perfctr...
  killall likwid-perfctr

  killall java-migrator
  

 # echo Stopping power monitor...
 # /afs/cs.pitt.edu/usr0/vpetrucci/stop-power-mon.sh

 # sleep 2
 # sync

 # cp /afs/cs.pitt.edu/usr0/vpetrucci/disk2/power-perf-quickia/power.txt $path/disk2/power-perf-quickia/${data}/power-$type-$a.txt
  #cp /ramcache/times $path/disk2/perf-quickia/${data}/times-$type-$a.txt
  mkdir $full_path/$interval-$c
  mv /ramcache/perf-$a.txt $full_path/$interval-$c/
  mv /afs/cs.pitt.edu/usr0/vpetrucci/faban-output/* $full_path/$interval-$c/

  sync

  echo Done.
  echo

  sleep 5
 done
done
