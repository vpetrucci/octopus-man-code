#
#     Vinicius Petrucci, UCSD 
#     2013
#
#

#apps=('calculix' 'hmmer' 'mcf' 'lbm' 'milc' 'soplex' 'povray' 'libquantum')

#apps=('calculix' 'lbm' 'hmmer' 'milc' 'libquantum' 'povray' 'tonto' 'gobmk')

apps=('calculix' 'lbm' 'hmmer' 'milc' 'libquantum' 'povray' 'tonto' 'gobmk' 'gromacs' 'namd' 'astar' 'cactusADM' 'soplex' 'leslie3d' 'zeusmp' 'sjeng')

#apps=('GemsFDTD' 'hmmer' 'gobmk' 'cactusADM' 'tonto' 'bwaves' 'lbm' 'bzip2' 'leslie3d' 'gromacs' 'sjeng' 'calculix' 'astar' 'zeusmp' 'povray' 'mcf' 'namd' 'libquantum' 'gamess' 'soplex' 'milc')

path="/afs/cs.pitt.edu/usr0/vpetrucci/"
data=`date +%Y-%m-%d-%H%M`
full_path=$path/disk2/websearch-quickia/${data}
mkdir -p $full_path

cd /ramcache/

for type in 'big' 'small';
do
    
for c in 5 10 15 20 25 30 35 40 45 50 ;
#for c in 5 25 50 75 100
#for c in 15 35;
do

for a in "${apps[@]}";
do

#  echo Starting power monitor...
#  /afs/cs.pitt.edu/usr0/vpetrucci/start-power-mon.sh
#  sleep 2

  cur_date=`date +%Y-%m-%d`
  echo -n > /ramcache/logs/localhost_access_log.$cur_date.txt
  
  # change num of clients
  sed -i  -e 's#\(<fa:scale>\)[0-9]*\(</fa:scale>\)#\1'$c'\2#g' /afs/cs.pitt.edu/usr0/vpetrucci/deploy/run.xml
  sync
  
  echo Starting performance monitor...
  if [ $type == big ];
  then
#    taskset -c 5 /afs/cs.pitt.edu/usr0/vpetrucci/likwid-3.0/likwid-perfctr -o perf-big-$a.txt -t 1s -c 3 -g INSTR_RETIRED_ANY:FIXC0,L2_LINES_IN_THIS_CORE_ALL:PMC0,BUS_TRANS_MEM_THIS_CORE_THIS_A:PMC1 &
    #taskset -c 5 /afs/cs.pitt.edu/usr0/vpetrucci/likwid-3.0/likwid-perfctr -o perf-big-$a.txt -t 1s -c 3 -g INSTR_RETIRED_ANY:FIXC0,L1D_REPL:PMC0,L2_LINES_IN_THIS_CORE_ALL:PMC1 &
    sleep 10 && taskset -c 5 /afs/cs.pitt.edu/usr0/vpetrucci/likwid-3.0/likwid-perfctr -o perf-big-search-$a.txt -t 1s -c 2,4 -g INSTR_RETIRED_ANY:FIXC0,L2_RQSTS_SELF_MESI:PMC0,L2_LINES_IN_THIS_CORE_ALL:PMC1 &
    #taskset -c 5 /afs/cs.pitt.edu/usr0/vpetrucci/likwid-3.0/likwid-perfctr -o perf-big-$a.txt -t 1s -c 4 -g INSTR_RETIRED_ANY:FIXC0,RESOURCE_STALLS_ANY:PMC0,RAT_STALLS_ANY:PMC1 &
  else
#    taskset -c 5 /afs/cs.pitt.edu/usr0/vpetrucci/likwid-3.0/likwid-perfctr -o perf-small-$a.txt -t 1s -c 0 -g INSTR_RETIRED_ANY:FIXC0,L1D_REPL:PMC0,L2_LINES_IN_THIS_CORE_ALL:PMC1 &
     sleep 10 && taskset -c 5 /afs/cs.pitt.edu/usr0/vpetrucci/likwid-3.0/likwid-perfctr -o perf-small-search-$a.txt -t 1s -c 0,1 -g INSTR_RETIRED_ANY:FIXC0,L2_RQSTS_SELF_MESI:PMC0,L2_LINES_IN_THIS_CORE_ALL:PMC1 &
  fi
  #sleep 1
  
   #   echo "Running websearch on small cores..."
    #  /afs/cs.pitt.edu/usr0/vpetrucci/all-java-to-small-cores-loop.sh > /dev/null & pid1=$! 
   #   echo "Running SPEC on BIG cores"     
    
   
  if [ $type == big ];
  then
     /afs/cs.pitt.edu/usr0/vpetrucci/move-java-jobs.sh 2     
     taskset -c 4 python $path/run-apps2.py $a   & pid4=$!      
  else
     /afs/cs.pitt.edu/usr0/vpetrucci/move-java-jobs.sh 0     
     taskset -c 1 python $path/run-apps2.py $a   & pid4=$!        	  
   fi     
  
  taskset -c 3 /afs/cs.pitt.edu/usr0/vpetrucci/start-faban-remotely.sh

  ps1=`ps -P ax | grep run-apps | egrep 'S[^+]' | cut -f1 -d" "`
  echo $ps1
  kill $ps1

  ps1=`ps -P ax | grep run-apps | egrep 'S[^+]' | cut -f2 -d" "`
  echo $ps1
  kill $ps1
  
  kill $pid4
       
  killall likwid-perfctr

  sleep 1
  echo pidof:`pidof likwid-perfctr`
  
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
  
  sh /afs/cs.pitt.edu/usr0/vpetrucci/kill-experiment.sh
  
 # echo Stopping power monitor...
 # /afs/cs.pitt.edu/usr0/vpetrucci/stop-power-mon.sh

 # sleep 2
 # sync

 # cp /afs/cs.pitt.edu/usr0/vpetrucci/disk2/power-perf-quickia/power.txt $path/disk2/power-perf-quickia/${data}/power-$type-$a.txt
  #cp /ramcache/times $path/disk2/perf-quickia/${data}/times-$type-$a.txt
  mkdir $full_path/$type-$c
  mv /ramcache/perf-$type-search-$a.txt $full_path/$type-$c/
  mv /afs/cs.pitt.edu/usr0/vpetrucci/faban-output/* $full_path/$type-$c/
  cp /ramcache/logs/localhost_access_log.$cur_date.txt $full_path/$type-$c/localhost_access_log.$type-$a.txt

  sync

  echo Done.
  echo

  sleep 10
 done
done
done


