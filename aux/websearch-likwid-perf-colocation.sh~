#
#     Vinicius Petrucci, UCSD 
#     2013
#
#

apps=('calculix' 'hmmer' 'mcf' 'lbm' 'astar' 'soplex' 'povray' 'libquantum')

#apps=('GemsFDTD' 'hmmer' 'gobmk' 'cactusADM' 'tonto' 'bwaves' 'lbm' 'bzip2' 'leslie3d' 'gromacs' 'sjeng' 'calculix' 'astar' 'zeusmp' 'povray' 'mcf' 'namd' 'libquantum' 'gamess' 'soplex' 'milc')

path="/afs/cs.pitt.edu/usr0/vpetrucci/"
data=`date +%Y-%m-%d-%H%M`
full_path=$path/disk2/websearch-quickia/${data}
mkdir -p $full_path

cd /ramcache/

for a in "${apps[@]}";
do

for type in 'big' 'small';
do

for c in 25 50 100 150 200;
#for c in 250;
do

#  echo Starting power monitor...
#  /afs/cs.pitt.edu/usr0/vpetrucci/start-power-mon.sh
#  sleep 2

  # change num of clients
  sed -i  -e 's#\(<fa:scale>\)[0-9]*\(</fa:scale>\)#\1'$c'\2#g' /afs/cs.pitt.edu/usr0/vpetrucci/deploy/run.xml
  sync
  
  echo Starting performance monitor...
  if [ $type == big ];
  then
#    taskset -c 5 /afs/cs.pitt.edu/usr0/vpetrucci/likwid-3.0/likwid-perfctr -o perf-big-$a.txt -t 1s -c 3 -g INSTR_RETIRED_ANY:FIXC0,L2_LINES_IN_THIS_CORE_ALL:PMC0,BUS_TRANS_MEM_THIS_CORE_THIS_A:PMC1 &
    #taskset -c 5 /afs/cs.pitt.edu/usr0/vpetrucci/likwid-3.0/likwid-perfctr -o perf-big-$a.txt -t 1s -c 3 -g INSTR_RETIRED_ANY:FIXC0,L1D_REPL:PMC0,L2_LINES_IN_THIS_CORE_ALL:PMC1 &
    sleep 5 && taskset -c 5 /afs/cs.pitt.edu/usr0/vpetrucci/likwid-3.0/likwid-perfctr -o perf-big-search-$a.txt -t 1s -c 0,1,2,4 -g INSTR_RETIRED_ANY:FIXC0,L2_RQSTS_SELF_MESI:PMC0,L2_LINES_IN_THIS_CORE_ALL:PMC1 &
    #taskset -c 5 /afs/cs.pitt.edu/usr0/vpetrucci/likwid-3.0/likwid-perfctr -o perf-big-$a.txt -t 1s -c 4 -g INSTR_RETIRED_ANY:FIXC0,RESOURCE_STALLS_ANY:PMC0,RAT_STALLS_ANY:PMC1 &
  else
#    taskset -c 5 /afs/cs.pitt.edu/usr0/vpetrucci/likwid-3.0/likwid-perfctr -o perf-small-$a.txt -t 1s -c 0 -g INSTR_RETIRED_ANY:FIXC0,L1D_REPL:PMC0,L2_LINES_IN_THIS_CORE_ALL:PMC1 &
    sleep 5 && taskset -c 5 /afs/cs.pitt.edu/usr0/vpetrucci/likwid-3.0/likwid-perfctr -o perf-small-search-$a.txt -t 1s -c 0,1,2,4 -g INSTR_RETIRED_ANY:FIXC0,L2_RQSTS_SELF_MESI:PMC0,L2_LINES_IN_THIS_CORE_ALL:PMC1 &

  fi
  #sleep 1
  
  if [ $type == big ];
  then
      echo "Running websearch on big cores..."
      /afs/cs.pitt.edu/usr0/vpetrucci/all-java-to-big-cores-loop.sh > /dev/null & pid1=$!  
      echo "Running SPEC on small cores"     
      taskset -c 0 python $path/run-apps2.py $a   & pid2=$!
      sleep 2
      taskset -c 1 python $path/run-apps2-copy.py $a   & pid3=$!
  else
      echo "Running websearch on small cores..."
      /afs/cs.pitt.edu/usr0/vpetrucci/all-java-to-small-cores-loop.sh > /dev/null & pid1=$! 
      echo "Running SPEC on BIG cores"     
      taskset -c 2 python $path/run-apps2.py $a   & pid2=$!
      sleep 2
      taskset -c 4 python $path/run-apps2-copy.py $a    &   pid3=$!       
  fi
  
  taskset -c 3 /afs/cs.pitt.edu/usr0/vpetrucci/start-faban-remotely.sh

  ps1=`ps -P ax | grep run-apps | egrep 'S[^+]' | cut -f1 -d" "`
  echo $ps1
  kill $ps1

  ps1=`ps -P ax | grep run-apps | egrep 'S[^+]' | cut -f2 -d" "`
  echo $ps1
  kill $ps1
  
  kill $pid1
  kill $pid2
  kill $pid3

  ps1=`ps -P ax | grep run-apps | egrep 'S[^+]' | cut -f1 -d" "`
  echo $ps1
  kill $ps1

  ps1=`ps -P ax | grep run-apps | egrep 'S[^+]' | cut -f2 -d" "`
  echo $ps1
  kill $ps1
       
  killall likwid-perfctr

  sleep 1
  echo pidof:`pidof likwid-perfctr`
  
  ps3=`ps -P ax | grep cpu2006 | egrep 'R[^+]' | cut -f1 -d" "`
  echo $ps3
  kill $ps3

  ps3=`ps -P ax | grep cpu2006 | egrep 'R[^+]' | cut -f2 -d" "`
  echo $ps3
  kill $ps3
 

 # echo Stopping power monitor...
 # /afs/cs.pitt.edu/usr0/vpetrucci/stop-power-mon.sh

 # sleep 2
 # sync

 # cp /afs/cs.pitt.edu/usr0/vpetrucci/disk2/power-perf-quickia/power.txt $path/disk2/power-perf-quickia/${data}/power-$type-$a.txt
  #cp /ramcache/times $path/disk2/perf-quickia/${data}/times-$type-$a.txt
  mkdir $full_path/$type-$c
  mv /ramcache/perf-$type-search-$a.txt $full_path/$type-$c/
  mv /afs/cs.pitt.edu/usr0/vpetrucci/faban-output/* $full_path/$type-$c/

  sync

  echo Done.
  echo

  sleep 5
 done
done
done
