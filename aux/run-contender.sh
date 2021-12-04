
path="/afs/cs.pitt.edu/usr0/vpetrucci/"

taskset -c 0 python $path/run-apps.py lbm &
taskset -c 2 python $path/run-apps.py lbm &
taskset -c 4 python $path/run-apps.py lbm &
taskset -c 6 python $path/run-apps.py lbm &

