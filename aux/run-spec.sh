
wload[0]="4CI"
wload[1]="3CI-1MI"
wload[2]="2CI-2MI"
wload[3]="1CI-3MI"
wload[4]="4MI"
wload[5]="4P"

apps[0]="calculix gamess namd tonto"
apps[1]="gamess sjeng bwaves soplex"
apps[2]="bwaves tonto soplex mcf"
apps[3]="sjeng lbm milc soplex"
apps[4]="lbm milc GemsFDTD soplex"
apps[5]="astar bwaves sjeng milc"

host=`hostname | cut -d. -f1`

path="/afs/cs.pitt.edu/usr0/vpetrucci/"
data=`date +%Y-%m-%d-%H%M`
mkdir -p $path/disk2/perf-results-$host/${data}

rm /ramcache/core* -rf

for b in GemsFDTD  astar  bwaves  bzip2  cactusADM  calculix  povray gromacs lbm  leslie3d  mcf  milc  namd  sjeng  soplex  tonto  zeusmp;
do 

  # monitor big core
  taskset -c 0 $path/perf2 stat -a -C 0 -e rc0 -e r4008317e1 -e r4008327e1 -e r4008347e1 -e r4008387e1 -f -o /ramcache/core_0 &
  taskset -c 2 $path/perf2 stat -a -C 2,4,6 -e rc0 -f -o /ramcache/core_other  &

  /usr/bin/time -p -o $path/disk2/perf-results-$host/${data}/time.big.$b taskset -c 0 python $path/run-apps.py $b
  sleep 1
  killall perf2
  sleep 1

  mv /ramcache/core_0 $path/disk2/perf-results-$host/${data}/core_0.big.$b
  mv /ramcache/core_other $path/disk2/perf-results-$host/${data}/core_other.big.$b
  killall $b"_base.amd64-m64-gcc42-nn"

  sleep 10

  # monitor small core
  taskset -c 0 $path/perf2 stat -a -C 0 -e rc0 -e r4008317e1 -e r4008327e1 -e r4008347e1 -e r4008387e1 -f -o /ramcache/core_0  &
  taskset -c 2 $path/perf2 stat -a -C 2,4,6 -e rc0 -f -o /ramcache/core_other  &

  /usr/bin/time -p -o $path/disk2/perf-results-$host/${data}/time.small.$b taskset -c 2 python $path/run-apps.py $b
  sleep 1
  killall perf2
  sleep 1

  mv /ramcache/core_0 $path/disk2/perf-results-$host/${data}/core_0.small.$b
  mv /ramcache/core_other $path/disk2/perf-results-$host/${data}/core_other.small.$b
  killall $b"_base.amd64-m64-gcc42-nn"
  sleep 10

done



