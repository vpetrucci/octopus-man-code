

taskset -c 0 /afs/cs.pitt.edu/usr0/vpetrucci/disk2/search-release/faban/search/run.sh & pid=$!

sleep 20

for i in `ps -P ax | grep faban | cut -f1 -d" "`; do 
    taskset -c -p 3 $i; 
      for i in $i; do
        child_i=`ls /proc/$i/task/`
        for j in $child_i; do taskset -c -p 3 $j; done
      done
done

wait $pid
