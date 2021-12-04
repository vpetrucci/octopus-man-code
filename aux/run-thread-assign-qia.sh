#
#     Vinicius Petrucci, UCSD 
#     2013
#
#

wload[0]="4CI"
wload[1]="3CI-1MI"
wload[2]="2CI-2MI"
wload[3]="1CI-3MI"
wload[4]="4MI"
wload[5]="4P"
#wload[6]="4PM"
#wload[7]="4PC"
#wload[6]="2P2M"
#wload[7]="2P2C"

apps[0]="calculix gamess namd hmmer"
apps[1]="povray sjeng bwaves libquantum"
apps[2]="calculix hmmer milc lbm"
apps[3]="hmmer lbm milc soplex"
apps[4]="lbm milc mcf libquantum"
apps[5]="astar bzip2 milc tonto"
#apps[5]="astar bzip2 leslie3d milc"
#apps[6]="namd mcf astar bwaves"
#apps[7]="lbm bzip2 calculix GemsFDTD"

host="quickia"

#for m in 50 100 250 500;
#for m in 100 250 500;
for m in 100;
#for m in 500;
do

path="/afs/cs.pitt.edu/usr0/vpetrucci/"
data=`date +%Y-%m-%d-%H%M`
full_path=$path/disk2/new-results-$host/${data}-$m

mkdir -p $full_path

# monitor
#taskset -c 0 $path/perf2 stat -a -C 0 -e rc0 -e r4008317e1 -e r4008327e1 -e r4008347e1 -e r4008387e1 -o /ramcache/core_0 -s $m &
#taskset -c 2 $path/perf2 stat -a -C 2,4,6 -e rc0 -o /ramcache/core_other -s $m &

# small( 0 1 ) big( 2 4 )

taskset -c 3 /afs/cs.pitt.edu/usr0/vpetrucci/likwid-3.0/likwid-perfctr -f -o /ramcache/perfdata.txt -t ${m}ms -c 0,1,2,4 -g INSTR_RETIRED_ANY:FIXC0,L2_RQSTS_SELF_MESI:PMC0,L2_LINES_IN_THIS_CORE_ALL:PMC1 &

let interval=$m*2

#echo "running schemes: " $*

#for k in `seq 0 5`;
#for k in `seq 2 5`;
for k in 0;
#for k in 5 4 3 2 1 0;
#for k in `seq 0 0`;
do
# for i in `seq 0 1`;
# for i in `seq 1 2`;
# for i in `seq 0 4`;
#for i in 0 1 2 3 4 5;
for i in 3 4 0;
# for i in 0 1 2 3 4 5;
# for i in 2;
# for i in $*;
 do
  echo ".........................."
  ps ax | grep cpu2006 | egrep 'R[^+]' 
  echo ".........................."
  echo "running workload ${wload[k]} with apps ${apps[k]}"
  taskset -c 0,1,2,4 python $path/run-apps.py ${apps[k]} &
  sleep 10
  $path/thread_assign-qia $i $interval
  mv /ramcache/mapping $full_path/mapping.$i.${wload[k]}
  mv /ramcache/times $full_path/times.$i.${wload[k]}
  mv /ramcache/stats $full_path/stats.$i.${wload[k]}
  sleep 2
  for x in `seq 0 5`; do for y in ${apps[x]}; do killall $y"_base.amd64-m64-gcc42-nn"; done; done
  kill `ps -P ax | grep run-apps | egrep 'S[^+]' | cut -f1 -d" "`
  kill `ps -P ax | grep cpu2006 | egrep 'R[^+]' | cut -f1 -d" "`
  kill `ps -P ax | grep run-apps | egrep 'S[^+]' | cut -f2 -d" "`
  kill `ps -P ax | grep cpu2006 | egrep 'R[^+]' | cut -f2 -d" "`
  sleep 2
 done
done

# clean up
#rm /ramcache/* -rf
#killall perf2
killall likwid-perfctr
sleep 1
echo pidof:`pidof likwid-perfctr`

ps1=`ps -P ax | grep run-apps | egrep 'S[^+]' | cut -f1 -d" "`
kill $ps1
ps3=`ps -P ax | grep cpu2006 | egrep 'R[^+]' | cut -f1 -d" "`
kill $ps3
    
sleep 10

done


