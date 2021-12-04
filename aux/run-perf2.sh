
taskset -c 0 /afs/cs.pitt.edu/usr0/vpetrucci/perf2 stat -a -C 0 -e rc0 -e r4008317e1 -e r4008327e1 -e r4008347e1 -e r4008387e1 -o /ramcache/core_0 -s 100 &
taskset -c 2 /afs/cs.pitt.edu/usr0/vpetrucci/perf2 stat -a -C 2,4,6 -e rc0 -o /ramcache/core_other -s 100 &

