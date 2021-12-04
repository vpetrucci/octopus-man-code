
import sys
import os
import time
from copy import copy

# long running processes
#job_pids = [19216, 19272, 19410, 19530, 19587]
job_pids = [int(p) for p in os.popen('ps ax | grep java | cut -d" " -f1 | head -5').readlines()]

print 'job_pids', job_pids


# core performance factor
perf_factor = [1.0, 1.0, 2.0, 2.0, 2.0, 2.0]
prop_factor = [16.0, 17.0, 33.0, 34.0]
    
#user_util = 100 * (utime_after - utime_before) / (time_total_after - time_total_before);
#sys_util = 100 * (stime_after - stime_before) / (time_total_after - time_total_before);

# You could use sampling kind of stuff here. Read ctime and utime for a PID at a point in time and read the same values again after 1 sec. 
# Find the difference and divide by hundred. You will get utilization for that process for past one second.
 
def cpu_total_time():
    try:
        f = file('/proc/stat', 'r')
        s = f.readlines()
        f.close()
    except IOError:
        return -1
    return sum([int(i) for i in s[0].split(' ')[2:]])
        
def which_core(pid):
    try:
        f = file(os.path.join('/proc', str(pid), 'stat'), 'rb')
        s = f.read()
        f.close()
    except IOError:
        return -1
    return int(s.split(' ')[-6])

def is_running(pid):
    try:
        f = file(os.path.join('/proc', str(pid), 'stat'), 'rb')
        s = f.read()
        f.close()
    except IOError:
        return -1
    stat = s.split(' ')[2]
    if stat == 'R':
        return 1
    else:
        return 0

def task_time(pid):
    try:
        f = file(os.path.join('/proc', str(pid), 'stat'), 'rb')
        s = f.read()
        f.close()
    except IOError:
        return -1
    utime = int(s.split(' ')[13])
    return utime
        
def imbal_factor(core_load):
    imbal = 0
    core_list = core_load.keys()
    for i in range(len(core_list)-1):
        for j in range(i+1, len(core_list)):
            imbal += abs(core_load[core_list[i]]/perf_factor[i] - core_load[core_list[j]]/perf_factor[j])
    return imbal    

def job_task_list(pid):
    #return os.listdir('/proc/'+str(pid)+'/task/')
    return [int(i) for i in os.listdir('/proc/'+str(p)+'/task/')]
    
#def move_task(c1, c2):


while True:
    
    # all tasks of a job
    task_list_all = {}
    
    # only tasks that are active running
    task_list = {}
    task_list_size = []
    total_task = 0
    
    # thread-to-core mapping
    task_map = {}
    
    # task parent info
    task_parent = {}
    
    # per core info
    core_task = {}

    # measure task CPU time
    total_time_before = cpu_total_time()
    task_time_before = {}
    for p in job_pids:
        task_list_all[p] = job_task_list(p)
        for t in task_list_all[p]:
            task_time_before[t] = task_time(t)
    #time.sleep(1)
    print 'a'
    total_time_after = cpu_total_time()
    task_util = {}
    for p in job_pids:
        for t in task_list_all[p]:
            task_util[t] = (task_time(t) - float(task_time_before[t])) / float(total_time_after - total_time_before);
            
    # get task list for each process
    # identify where each task is running on
    # update: only add task that is "running" (> 5\% of CPU utilization)
    for p in job_pids:
        for t in task_list_all[p]:
         #   if not is_running(t): continue
            if task_util[t] < 0.05: continue
            #print p, task_list
            if p not in task_list: task_list[p] = []
            task_list[p] += [t]
            #print task_list[p]
            #print p,t,which_core(t)
            task_parent[t] = p
            core_t = which_core(t)
            task_map[t] = core_t
            if core_t not in core_task: core_task[core_t] = []
            core_task[core_t] += [t]
        #print task_list
        if task_list != {}:
            task_list_size += [(len(task_list[p]), p)]
            total_task += len(task_list[p])
    
    # compute core load    
    # core scaled load is given by the number of running threads on it divided by the core perf factor
    core_load = {}
    core_load_list = []
    for c,l in core_task.items(): 
      #  print 'perf_factor',c,perf_factor[c]
      #  print 'len(l)', c,len(l)
        core_load[c] = len(l) / float(perf_factor[c])
        core_load_list += [(len(l) / float(perf_factor[c]), c)]
    core_load_list.sort(reverse=True)
    
    #print 'core_load_list', core_load_list
    
    #print 'total_task', total_task
    #print 'core_load', core_load
    #print 'task_list_size', sorted(task_list_size, reverse=True)
    #print 'imbal_factor', imbal_factor(core_load)
    
    # load balancing algorithm
    
    #total_perf_factor = sum([1,1,2,2])
    
    cur_imbal_factor = imbal_factor(core_load)
    print 'a..'
    while True:
        
        if cur_imbal_factor == 0: break
        
        most_loaded_core = core_load_list[0][1]
        least_loaded_core = core_load_list[-1][1]
     #   print 'least_loaded', least_loaded_core
     #   print 'most_loaded', most_loaded_core
    
        # build new core task
        new_core_task = copy(core_task)
    
        # swap threads
        t = new_core_task[most_loaded_core].pop()
        new_core_task[least_loaded_core] += [t]
        
        # compute new core load
        new_core_load = {}
        new_core_load_list = []
        for c,l in new_core_task.items(): 
            new_core_load[c] = len(l) / perf_factor[c]
            new_core_load_list += [(len(l) / perf_factor[c], c)]
        new_core_load_list.sort(reverse=True)
        
        # compute new imbal factor
        new_imbal_factor = imbal_factor(new_core_load)
    
     #   print 'cur_imbal_factor', cur_imbal_factor
     #   print 'new_imbal_factor', new_imbal_factor
        
        # keep solution if improved
        if new_imbal_factor < cur_imbal_factor:
            core_load_list = new_core_load_list
            core_task = new_core_task
            cur_imbal_factor = new_imbal_factor
            core_load = new_core_load
      #      print 'move pid', t, 'from core', most_loaded_core, 'to core', least_loaded_core
            os.system('taskset -c -p ' + str(least_loaded_core) + ' ' + str(t) + ' > /dev/null')
        else:
            break
    
    print 'core_load', core_load

