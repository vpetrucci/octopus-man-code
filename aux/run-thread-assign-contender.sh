
wload[0]="4CI"
wload[1]="3CI-1MI"
wload[2]="2CI-2MI"
wload[3]="1CI-3MI"
wload[4]="4MI"
wload[5]="4P"
wload[6]="4R1"
wload[7]="4R2"

apps[0]="calculix povray namd tonto"
apps[1]="povray sjeng bwaves soplex"
apps[2]="bwaves tonto soplex mcf"
apps[3]="sjeng lbm milc soplex"
apps[4]="lbm milc GemsFDTD soplex"
apps[5]="astar bzip2 leslie3d milc"
apps[6]="astar namd mcf leslie3d"
apps[7]="lbm bzip2 calculix GemsFDTD"

host=`hostname | cut -d. -f1`

export GRB_LICENSE_FILE=/afs/cs.pitt.edu/usr0/vpetrucci/gurobi.lic.$host

#for m in 50 100 250 500;
for m in 100;
do

path="/afs/cs.pitt.edu/usr0/vpetrucci/"
data=`date +%Y-%m-%d-%H%M`
mkdir -p $path/disk2/results-$host/${data}-$m

# monitor
taskset -c 0 $path/perf2 stat -a -C 0 -e rc0 -e r4008317e1 -e r4008327e1 -e r4008347e1 -e r4008387e1 -o /ramcache/core_0 -s $m &
taskset -c 2 $path/perf2 stat -a -C 2,4,6 -e rc0 -o /ramcache/core_other -s $m &

let interval=$m*2

#taskset -c 0 python $path/run-apps2.py milc &
#taskset -c 2 python $path/run-apps2.py milc &
#taskset -c 4 python $path/run-apps2.py milc &
#taskset -c 6 python $path/run-apps2.py milc &

taskset -c 0 $path/lmbench3/bin/x86_64-linux-gnu/stream -M 60000000 -N 9999999999  &
taskset -c 2 $path/lmbench3/bin/x86_64-linux-gnu/stream -M 60000000 -N 9999999999  &
taskset -c 4 $path/lmbench3/bin/x86_64-linux-gnu/stream -M 60000000 -N 9999999999  &
taskset -c 6 $path/lmbench3/bin/x86_64-linux-gnu/stream -M 60000000 -N 9999999999  &

#sleep 5

echo "running schemes: " $*

#for k in `seq 0 5`;
for k in 5 4 3 2 1 0;
#for k in `seq 0 0`;
do
# for i in `seq 0 1`;
# for i in `seq 1 2`;
# for i in `seq 0 4`;
# for i in 1 4 3;
 for i in $*;
 do
  python $path/run-apps.py ${apps[k]} &
  sleep 10
  $path/thread_assign2 $i $interval
  mv /ramcache/mapping $path/disk2/results-$host/${data}-$m/mapping.$i.${wload[k]}
  mv /ramcache/times $path/disk2/results-$host/${data}-$m/times.$i.${wload[k]}
  mv /ramcache/stats $path/disk2/results-$host/${data}-$m/stats.$i.${wload[k]}
  sleep 10
  #for x in `seq 0 5`; do for y in ${apps[x]}; do killall $y"_base.amd64-m64-gcc42-nn"; done; done
  #sleep 10
 done
done

# clean up
rm /ramcache/* -rf
killall perf2

sleep 10

done


