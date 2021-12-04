#
#  Task mapper for heterogeneous processor systems
#  Vinicius Petrucci, UCSD
#  2013

import os
import time
import pickle
import sys
import threading, Queue, subprocess
import signal
import psutil
import math
import random

# import psutil
# somepid = 1023
# p = psutil.Process(somepid)
# p.suspend()
# p.resume()

from scipy import stats

AVG_BIG_POWER	= 15.63
AVG_SMALL_POWER	= 1.60
PEAK_BIG_POWER	= 18.75
PEAK_SMALL_POWER = 2.15
IDLE_BIG_POWER	= 9.625
IDLE_SMALL_POWER = 0.7

LLC_WAKE_POWER = 1.2
LLC_ACT_POWER = 1.5
BIG_MAX_LLC = 70808.47
SMALL_MAX_LLC = 38049.55

BIG_MIPS = 2558.72
SMALL_MIPS  = 1216.6

#SMALL_THR = 0.65
#BIG_THR = 0.35

#DELAY_UP_THR = 0.7
#DELAY_DOWN_THR = 0.3
#TARGET_DELAY = 200

#SLEEP_INTERVAL = 15
#ALPHA = 0.15

SMALL_SOCKET_THR = 60 # QPS
#QOS_THR = 0.95

SEARCH_LLCM_THR = 3930.88
BATCH_LLCM_THR = 7335.83

HYST_FACTOR = 3
hyst_count = 0

#search_LLCM < 3930.88 : 0 (13/0)
#search_LLCM >= 3930.88
#|   batch_LLCM < 7335.83 : 0 (2/0)
#|   batch_LLCM >= 7335.83 : 1 (3/0)

#(search_LLCM >= 3880.487) and (batch_LLCM >= 9219.18) => qos_degrad=1 (5.0/0.0)
# => qos_degrad=0 (58.0/1.0)

#search_LLCM >= 4383.8

if len(sys.argv) < 7:
    print 'please specify: policy interval deadline up_thr down_thr alpha app'
    sys.exit(2)

policy = sys.argv[1]
print 'policy = ', policy
    
SLEEP_INTERVAL = int(sys.argv[2])
print 'SLEEP_INTERVAL = ', SLEEP_INTERVAL

TARGET_DELAY = int(sys.argv[3])
print 'TARGET_DELAY = ', TARGET_DELAY

DELAY_UP_THR = float(sys.argv[4])
print 'DELAY_UP_THR = ', DELAY_UP_THR

DELAY_DOWN_THR = float(sys.argv[5])
print 'DELAY_DOWN_THR = ', DELAY_DOWN_THR

ALPHA = float(sys.argv[6])
print 'ALPHA = ', ALPHA

APP = str(sys.argv[7])
print 'APP = ', APP

SET_FACTOR = int(sys.argv[8])
print 'SETTLING_FACTOR = ', SET_FACTOR

inc_factor = 0.05
deadband_factor = 0.00
               
def batch_pids():
    job_pids = [int(p) for p in os.popen("ps ax | grep cpu2006 | awk '{print $1}'").readlines()]
    to_rem = []
    for p in job_pids:
      if not os.path.exists('/proc/'+str(p)+'/task/'):
        to_rem += [p]
    for r in to_rem:
        job_pids.remove(r)
    return job_pids

def get_ppid(pid):
    try:
        f = file(os.path.join('/proc', str(pid), 'stat'), 'rb')
        s = f.read()
        f.close()
    except IOError:
        return -1
    return int(s.split(' ')[3])
    
def which_core(pid):
    try:
        f = file(os.path.join('/proc', str(pid), 'stat'), 'rb')
        s = f.read()
        f.close()
    except IOError:
        return -1
    return int(s.split(' ')[-6])


cpu_util = psutil.cpu_percent(SLEEP_INTERVAL, percpu=True)

paused_jobs_per_core = {}
job_paused = -1

big_qos_table = {}
small_qos_table = {}

settling_time = SET_FACTOR
settling_count = 0
is_settling = False

NUM_CORE_CONFIG = 4

# policies
# reactive, reactive_batch, static, static_batch


if APP == 'tomcat':

    avg_service_time = [46.43, 33.64, 22.64, 15.85]

    small_service_rate = 1/avg_service_time[0]*1000.0
    big_service_rate = 1/avg_service_time[2]*1000.0

    avg_service_rate = [small_service_rate, small_service_rate*2.0, big_service_rate, big_service_rate*2.0]

    #avg_service_rate = [1/i*1000 for i in avg_service_time]
    #  avg_slowdown = [i/avg_service_time[-1] for i in avg_service_time[:-1]]

    cdf_tab = []
    p90th_tab = []
    for c in range(NUM_CORE_CONFIG):
        cdf_load = []
        p90th_list = []
        for l in range(1,90):
            cdf = {}
            u = avg_service_rate[c]
            p90th_delay = 0.0
            for i in range(1,3000):
                r = float(i)/1000.0
                prob = 1 - math.exp(-(u-l)*(r))
                cdf[r] = prob
                if prob >= 0.90 and p90th_delay == 0.0:
                    p90th_delay = r*1000.0
            #print 'r', r
            cdf_load += [cdf]
            if p90th_delay == 0.0:
                #print 'config',c,'load', t,'l',l,'u',u,'p=',l/float(u)
                p90th_delay = 3000
            p90th_list += [p90th_delay]
        cdf_tab += [cdf_load]
        p90th_tab += [p90th_list]

elif APP == 'XXX':

    avg_service_time = [0.323126130952, 0.22349925641, 0.241003321429, 0.16754564557]

    small_service_rate = 1/(avg_service_time[0]/1000000.0)
    big_service_rate = 1/(avg_service_time[2]/1000000.0)

    avg_service_rate = [small_service_rate, small_service_rate*2.0, big_service_rate, big_service_rate*2.0]
    
    cdf_tab = []
    p95th_tab = []
    for c in range(NUM_CORE_CONFIG):
        cdf_load = []
        p95th_list = []
        for l in range(10,100000, 10):
            cdf = {}
            u = avg_service_rate[c]
            p95th_delay = 0.0
            for i in range(1,5000):
                r = float(i)/1000.0
                prob = 1 - math.exp(-(u-l)*(r))
                cdf[r] = prob
                if prob >= 0.95 and p95th_delay == 0.0:
                    p95th_delay = r*1000.0
            #print 'r', r
            cdf_load += [cdf]
            if p95th_delay == 0.0:
                #print 'config',c,'load', t,'l',l,'u',u,'p=',l/float(u)
                p95th_delay = 3000
            p95th_list += [p95th_delay]
        cdf_tab += [cdf_load]
        p95th_tab += [p95th_list]

#if policy == 'reactive':
#    app_alloc = [2,3]
#    os.system('/afs/cs.pitt.edu/usr0/vpetrucci/move-'+APP+'.sh 2,3 >/dev/null')
#    app_alloc = [0]
#    os.system('/afs/cs.pitt.edu/usr0/vpetrucci/move-'+APP+'.sh 0 >/dev/null')

if policy == 'reactive2':
    app_alloc = [2,3]
    os.system('/afs/cs.pitt.edu/usr0/vpetrucci/move-'+APP+'.sh 2,3 >/dev/null')

elif policy == 'qospred':
    app_alloc = [2,3]
    os.system('/afs/cs.pitt.edu/usr0/vpetrucci/move-'+APP+'.sh 2,3 >/dev/null')

elif policy == 'pidcontrol':
    app_alloc = [2,3]
    os.system('/afs/cs.pitt.edu/usr0/vpetrucci/move-'+APP+'.sh 2,3 >/dev/null')

elif policy == 'pidqoscontrol':
    app_alloc = [2,3]
    os.system('/afs/cs.pitt.edu/usr0/vpetrucci/move-'+APP+'.sh 2,3 >/dev/null')

elif policy == 'pidpred':
    app_alloc = [2,3]
    os.system('/afs/cs.pitt.edu/usr0/vpetrucci/move-'+APP+'.sh 2,3 >/dev/null')

elif policy == 'reactive_swap':
    app_alloc = [2,3]
    os.system('/afs/cs.pitt.edu/usr0/vpetrucci/move-'+APP+'.sh 2,3 >/dev/null')
        
elif policy == 'reactive_batch':
    app_alloc = [0, 1]
    os.system('/afs/cs.pitt.edu/usr0/vpetrucci/move-'+APP+'.sh 0,1 >/dev/null')
    os.system('/afs/cs.pitt.edu/usr0/vpetrucci/move-batch-jobs.sh 2,3 >/dev/null')

elif policy == 'static':
    app_alloc = [2, 3]
    os.system('/afs/cs.pitt.edu/usr0/vpetrucci/move-'+APP+'.sh 2,3 >/dev/null')

elif policy == 'static_wimpy':
    app_alloc = [0, 1]
    os.system('/afs/cs.pitt.edu/usr0/vpetrucci/move-'+APP+'.sh 0,1 >/dev/null')
        
elif policy == 'static_batch':
    app_alloc = [2, 3]
    os.system('/afs/cs.pitt.edu/usr0/vpetrucci/move-'+APP+'.sh 2,3 >/dev/null')
    os.system('/afs/cs.pitt.edu/usr0/vpetrucci/move-batch-jobs.sh 0,1 >/dev/null')

elif policy == 'reactive_batch_corun':
    os.system('/afs/cs.pitt.edu/usr0/vpetrucci/move-'+APP+'.sh 0,1 >/dev/null')
    b_pids = batch_pids()
    if len(b_pids) != 3:
        print 'OPS error... b_pids diff 3 !!!'
    else:
        os.system('taskset -c -p 1 ' + str(b_pids[0]))
        os.system('taskset -c -p 2 ' + str(b_pids[1]))
        os.system('taskset -c -p 4 ' + str(b_pids[2]))
        os.system('taskset -c -p 1 ' + str(get_ppid(b_pids[0])))
        os.system('taskset -c -p 2 ' + str(get_ppid(b_pids[1])))
        os.system('taskset -c -p 4 ' + str(get_ppid(b_pids[2])))
    app_alloc = [0]

elif policy == 'reactive_batch_energy':
    app_alloc = [0, 1]
    os.system('/afs/cs.pitt.edu/usr0/vpetrucci/move-batch-jobs.sh 0,1 >/dev/null')
    os.system('/afs/cs.pitt.edu/usr0/vpetrucci/move-'+APP+'.sh 0,1 >/dev/null')
    b_pids = batch_pids()
    for b in b_pids:
        p = psutil.Process(b)
        p.suspend()    

elif policy == 'reactive_batch_corun_energy':
    app_alloc = [0]
    os.system('/afs/cs.pitt.edu/usr0/vpetrucci/move-'+APP+'.sh 0 >/dev/null')
    os.system('/afs/cs.pitt.edu/usr0/vpetrucci/move-batch-jobs.sh 0,1 >/dev/null')    
    b_pids = batch_pids()
    if len(b_pids) != 2:
        print 'OPS error... b_pids diff 2 !!!'
    else:
 #       jobs_paused += [b_pids[0]]
        p = psutil.Process(b_pids[0])
        p.suspend() 
   
else:    
    app_alloc = [2,3]
    os.system('/afs/cs.pitt.edu/usr0/vpetrucci/move-'+APP+'.sh 2,3 >/dev/null')
 #   app_alloc = [0]
 #   os.system('/afs/cs.pitt.edu/usr0/vpetrucci/move-'+APP+'.sh 0 >/dev/null')
    
# PID control vars
integral = 0.0
previous_error = 0.0
output_max = 255
#output_max = 65535

prev_mapping = 3
mapping = 3
               
pid_theshold = 0.2

core_config = [[0], [0,1], [2], [2,3]]
               
def output_mapping(output):
    #    65536.0/4 = 16384
    # range(0,65536, 65536/4)
    #[0, 16384, 32768, 49152]
    
 #       if output >= 0 and output < 16384:
 #           return 3
 #       elif output >= 16384 and output < 32768:
 #           return 2
 #       elif output >= 32768 and output < 49152:
 #           return 1
 #       elif output >= 49152:
 #           return 0
    
    if output >= 0 and output < 64:
        return 3
    elif output >= 64 and output < 128:
        return 2
    elif output >= 128 and output < 192:
        return 1
    elif output >= 192:
        return 0

went_up = False
went_down = False

mon_file = open('/ramcache/hetero-mapper.txt', 'w')

prev_p95th_delay = 0.0
prev_avg_qps = 0.0

to_import = "monitor-"+APP
qos_monitor = __import__(to_import)

while True:

    keep_running = int(open('/ramcache/mapper_running').read())
    if not keep_running: break

    t1 = time.time() 
        
    #
    # read QoS
    #        
    avg_qps, avg_delay, p90th_delay, p95th_delay, p99th_delay= qos_monitor.read_values()
    
    print avg_qps, avg_delay, p95th_delay, p99th_delay    
    
    if avg_qps <= 0.0 or avg_delay <= 0.0 or p95th_delay <= 0.0 or p99th_delay <= 0.0:
        print 'waiting for QoS data from', APP
        time.sleep(SLEEP_INTERVAL)
        continue  

    print 'avg_qps', avg_qps
    print 'avg_delay (ms)', avg_delay
    print 'p90th_delay (ms)', p90th_delay
    print 'p95th_delay (ms)', p95th_delay
    print 'p99th_delay (ms)', p99th_delay
    print '-------- THRESHOLD ----------'
    print 'DELAY_UP_THR', DELAY_UP_THR
    print 'DELAY_DOWN_THR', DELAY_DOWN_THR
    print '-----------------------------'

    mon_file.write('%s; %.2f; %.2f; %.2f; %.2f; %.2f; %s; %.2f; %.2f; %.2f\n' % (str(cpu_util)[1:-1], avg_qps, avg_delay, p90th_delay, p95th_delay, p99th_delay, app_alloc, DELAY_UP_THR, DELAY_DOWN_THR, deadband_factor))
    mon_file.flush()

    cur_p95th_delay = p95th_delay
    
    # apply filter
    if prev_p95th_delay == 0.0:
        prev_p95th_delay = p95th_delay
    elif p95th_delay > 0.0:
        p95th_delay = ALPHA * p95th_delay + (1-ALPHA) * prev_p95th_delay
        prev_p95th_delay = p95th_delay

    print '------'
    print 'mapping', app_alloc
    print '------'

#    if is_settling:
#        settling_count += 1
#        if settling_count > settling_time:
#            is_settling = False
#            settling_count = 0
#        else:
#            print 'settling time...'
#            time.sleep(SLEEP_INTERVAL)
#            continue
        
    if policy == 'static':
        app_alloc = [2, 3]
        os.system('/afs/cs.pitt.edu/usr0/vpetrucci/move-'+APP+'.sh 2,3 >/dev/null')

    elif policy == 'static_wimpy':
        app_alloc = [0, 1]
        os.system('/afs/cs.pitt.edu/usr0/vpetrucci/move-'+APP+'.sh 0,1 >/dev/null')
        
    elif policy == 'static_batch':
        app_alloc = [2, 3]
        os.system('/afs/cs.pitt.edu/usr0/vpetrucci/move-'+APP+'.sh 2,3 >/dev/null')
        os.system('/afs/cs.pitt.edu/usr0/vpetrucci/move-batch-jobs.sh 0,1 >/dev/null')
    
    #elif policy == 'training90':
    #    if p90th_delay > TARGET_DELAY*DELAY_UP_THR:
                
    #    elif p90th_delay < TARGET_DELAY*DELAY_DOWN_THR:
                
    elif policy == 'reactive':

        if is_settling and settling_time > 0:       
          settling_count += 1
          print 'SETTLING TIME...', settling_count
          if settling_count >= settling_time:
            is_settling = False
            settling_count = 0          

        elif p90th_delay > TARGET_DELAY*DELAY_UP_THR:
            
            if app_alloc == [0]:
                os.system('/afs/cs.pitt.edu/usr0/vpetrucci/move-'+APP+'.sh 0,1 >/dev/null')
                app_alloc = [0,1]
                print 'moving to two small cores'
                is_settling = True
            elif app_alloc == [0,1]:
                os.system('/afs/cs.pitt.edu/usr0/vpetrucci/move-'+APP+'.sh 2 >/dev/null')
                app_alloc = [2]
                print 'moving to one big core'
                is_settling = True
            elif app_alloc == [2]:
                os.system('/afs/cs.pitt.edu/usr0/vpetrucci/move-'+APP+'.sh 2,3 >/dev/null')
                app_alloc = [2,3]
                print 'moving to two big cores'
                is_settling = True
             
        elif p90th_delay < TARGET_DELAY*DELAY_DOWN_THR:
            if app_alloc == [0,1]:
                os.system('/afs/cs.pitt.edu/usr0/vpetrucci/move-'+APP+'.sh 0 >/dev/null')
                app_alloc = [0]
                print 'moving BACK to one small core'
                is_settling = True
            elif app_alloc == [2]:
                os.system('/afs/cs.pitt.edu/usr0/vpetrucci/move-'+APP+'.sh 0,1 >/dev/null')
                app_alloc = [0,1]  
                print 'moving BACK to two small cores'
                is_settling = True
            elif app_alloc == [2,3]:
                os.system('/afs/cs.pitt.edu/usr0/vpetrucci/move-'+APP+'.sh 2 >/dev/null')
                app_alloc = [2]
                print 'moving BACK to one big core'
                is_settling = True

    elif policy == 'reactive95':
    
        if is_settling and settling_time > 0:       
          settling_count += 1
          print 'SETTLING TIME...', settling_count
          if settling_count >= settling_time:
            is_settling = False
            settling_count = 0          

        elif p95th_delay > TARGET_DELAY*DELAY_UP_THR:
            
            if app_alloc == [0]:
                os.system('/afs/cs.pitt.edu/usr0/vpetrucci/move-'+APP+'.sh 0,1 >/dev/null')
                app_alloc = [0,1]
                print 'moving to two small cores'
                is_settling = True
            elif app_alloc == [0,1]:
                os.system('/afs/cs.pitt.edu/usr0/vpetrucci/move-'+APP+'.sh 2 >/dev/null')
                app_alloc = [2]
                print 'moving to one big core'
                is_settling = True
            elif app_alloc == [2]:
                os.system('/afs/cs.pitt.edu/usr0/vpetrucci/move-'+APP+'.sh 2,3 >/dev/null')
                app_alloc = [2,3]
                print 'moving to two big cores'
                is_settling = True
             
        elif p95th_delay < TARGET_DELAY*DELAY_DOWN_THR:
            if app_alloc == [0,1]:
                os.system('/afs/cs.pitt.edu/usr0/vpetrucci/move-'+APP+'.sh 0 >/dev/null')
                app_alloc = [0]
                print 'moving BACK to one small core'
                is_settling = True
            elif app_alloc == [2]:
                os.system('/afs/cs.pitt.edu/usr0/vpetrucci/move-'+APP+'.sh 0,1 >/dev/null')
                app_alloc = [0,1]  
                print 'moving BACK to two small cores'
                is_settling = True
            elif app_alloc == [2,3]:
                os.system('/afs/cs.pitt.edu/usr0/vpetrucci/move-'+APP+'.sh 2 >/dev/null')
                app_alloc = [2]
                print 'moving BACK to one big core'
                is_settling = True
                
    elif policy == 'reactive95adapt':
        
        rand_num = random.random()
        if rand_num >= 0.995:
            if DELAY_DOWN_THR < 0.6:
                DELAY_DOWN_THR += 0.1        
                print '!!!! Setting new DELAY UP_THR to', DELAY_DOWN_THR 

        if is_settling and settling_time > 0:       
          settling_count += 1
          print 'SETTLING TIME...', settling_count
          if settling_count >= settling_time:
            is_settling = False
            settling_count = 0          
                   
        elif p95th_delay > TARGET_DELAY*DELAY_UP_THR:
                    
            if app_alloc == [0]:
                os.system('/afs/cs.pitt.edu/usr0/vpetrucci/move-'+APP+'.sh 0,1 >/dev/null')
                app_alloc = [0,1]
                print 'moving to two small cores'
                is_settling = True
            elif app_alloc == [0,1]:
                os.system('/afs/cs.pitt.edu/usr0/vpetrucci/move-'+APP+'.sh 2 >/dev/null')
                app_alloc = [2]
                print 'moving to one big core'
                is_settling = True
            elif app_alloc == [2]:
                os.system('/afs/cs.pitt.edu/usr0/vpetrucci/move-'+APP+'.sh 2,3 >/dev/null')
                app_alloc = [2,3]
                print 'moving to two big cores'
                # is_settling = True

            if went_down:
                if DELAY_DOWN_THR > 0.1:
                    DELAY_DOWN_THR -= 0.1        
                    print '!!!! Setting new DELAY DOWN_THR to',     DELAY_DOWN_THR  
                          
            went_down = False
             
        elif p95th_delay < TARGET_DELAY*DELAY_DOWN_THR:
        
            went_down = True
                        
            if app_alloc == [0,1]:
                os.system('/afs/cs.pitt.edu/usr0/vpetrucci/move-'+APP+'.sh 0 >/dev/null')
                app_alloc = [0]
                print 'moving BACK to one small core'
                is_settling = True
            elif app_alloc == [2]:
                os.system('/afs/cs.pitt.edu/usr0/vpetrucci/move-'+APP+'.sh 0,1 >/dev/null')
                app_alloc = [0,1]  
                print 'moving BACK to two small cores'
                is_settling = True
            elif app_alloc == [2,3]:
                os.system('/afs/cs.pitt.edu/usr0/vpetrucci/move-'+APP+'.sh 2 >/dev/null')
                app_alloc = [2]
                print 'moving BACK to one big core'
                is_settling = True

    elif policy == 'reactive90adapt':

        rand_num = random.random()
        if rand_num >= 0.995:
            if DELAY_DOWN_THR < 0.5:
                DELAY_DOWN_THR += 0.1        
                print '!!!! TRYING new DELAY DOWN_THR to', DELAY_DOWN_THR 
    
        if is_settling and settling_time > 0:       
          settling_count += 1
          print 'SETTLING TIME...', settling_count
          if settling_count >= settling_time:
            is_settling = False
            settling_count = 0          
                   
        elif p90th_delay > TARGET_DELAY*DELAY_UP_THR:
                    
            if app_alloc == [0]:
                os.system('/afs/cs.pitt.edu/usr0/vpetrucci/move-'+APP+'.sh 0,1 >/dev/null')
                app_alloc = [0,1]
                print 'moving to two small cores'
                is_settling = True
            elif app_alloc == [0,1]:
                os.system('/afs/cs.pitt.edu/usr0/vpetrucci/move-'+APP+'.sh 2 >/dev/null')
                app_alloc = [2]
                print 'moving to one big core'
                is_settling = True
            elif app_alloc == [2]:
                os.system('/afs/cs.pitt.edu/usr0/vpetrucci/move-'+APP+'.sh 2,3 >/dev/null')
                app_alloc = [2,3]
                print 'moving to two big cores'
                is_settling = True

            if went_up and went_down:
                if DELAY_DOWN_THR > 0.1:
                    DELAY_DOWN_THR -= 0.1        
                    print '!!!! Setting new DELAY DOWN_THR to',     DELAY_DOWN_THR  
                went_up = False    
            else:
                went_up = True
                              
            went_down = False
             
        elif p90th_delay < TARGET_DELAY*DELAY_DOWN_THR:
        
            went_down = True
                        
            if app_alloc == [0,1]:
                os.system('/afs/cs.pitt.edu/usr0/vpetrucci/move-'+APP+'.sh 0 >/dev/null')
                app_alloc = [0]
                print 'moving BACK to one small core'
                is_settling = True
            elif app_alloc == [2]:
                os.system('/afs/cs.pitt.edu/usr0/vpetrucci/move-'+APP+'.sh 0,1 >/dev/null')
                app_alloc = [0,1]  
                print 'moving BACK to two small cores'
                is_settling = True
            elif app_alloc == [2,3]:
                os.system('/afs/cs.pitt.edu/usr0/vpetrucci/move-'+APP+'.sh 2 >/dev/null')
                app_alloc = [2]
                print 'moving BACK to one big core'
                is_settling = True                
            
    elif policy == 'qospred':

        for i in range(NUM_CORE_CONFIG):
            pred_qos = p90th_tab[i][int(math.ceil(avg_qps))]
            #print 'cur_qos < qos_target', cur_qos, qos_target
            if pred_qos < TARGET_DELAY or i == 3:
                mapping = i
                break

        if mapping == 0:
            app_alloc = [0]
            os.system('/afs/cs.pitt.edu/usr0/vpetrucci/move-'+APP+'.sh 0 >/dev/null')
        elif mapping == 1:
            app_alloc = [0,1]
            os.system('/afs/cs.pitt.edu/usr0/vpetrucci/move-'+APP+'.sh 0,1 >/dev/null')
        elif mapping == 2:
            app_alloc = [2]
            os.system('/afs/cs.pitt.edu/usr0/vpetrucci/move-'+APP+'.sh 2 >/dev/null')
        elif mapping == 3:
            app_alloc = [2,3]
            os.system('/afs/cs.pitt.edu/usr0/vpetrucci/move-'+APP+'.sh 2,3 >/dev/null')

        print 'moving to', app_alloc

    elif policy == 'pidcontrol':
        
#        Kp = 1.5
        Kp = 0.11        
        Ki = 0.01
        Kd = 0.01
            
        #rand_num = random.random()
        #if rand_num >= 0.99:
        #    if deadband_factor > 0.0:
        #        deadband_factor -= 0.1
        #        if deadband_factor < 0.0: deadband_factor = 0.0       
        #        print '!!!! TRYING new deadband_factor:', deadband_factor

        dt = SLEEP_INTERVAL

#        error = TARGET_DELAY*0.8 - p90th_delay
        error = TARGET_DELAY - p90th_delay        
        #if error > 0:
        #    if (error / TARGET_DELAY) <= deadband_factor:
        #        error = 0
          #  else:
           #     error = error - 

#        if error > 0:
#            if (error / TARGET_DELAY) <= pid_threshold:
#                error = 0.0

        #print 'error', error
#        integral = integral + ((previous_error + error)/2.0)*dt
        integral = integral + error*dt

        if integral > output_max / Ki:
            integral = output_max / Ki
        elif integral < 0:
            integral = 0

        derivative = (error - previous_error)/dt
    
        output = Kp*error + Ki*integral + Kd*derivative
        previous_error = error
    
        if output < 0:
            output = 0
        elif output > output_max:
            output = output_max

        #print 'output', output
        
        mapping = output_mapping(output)

        app_alloc = core_config[mapping]

        # going up and it was down previously? bad!
        #if mapping > prev_mapping and went_down:
        #    if deadband_factor < 0.5:
        #        deadband_factor += 0.1       
        #        print '!!!! Setting new deadband_factor:',  deadband_factor            
        
        # going down ?
        #if mapping < prev_mapping:
        #    went_down = True
        #else:
        #    went_down = False
        
        #if mapping != prev_mapping:       
        print 'MOVING TO', app_alloc                
        if app_alloc == [0]:
            os.system('/afs/cs.pitt.edu/usr0/vpetrucci/move-'+APP+'.sh 0 >/dev/null')
        elif app_alloc == [0,1]:
            os.system('/afs/cs.pitt.edu/usr0/vpetrucci/move-'+APP+'.sh 0,1 >/dev/null')
        elif app_alloc == [2]:
            os.system('/afs/cs.pitt.edu/usr0/vpetrucci/move-'+APP+'.sh 2 >/dev/null')
        elif app_alloc == [2,3]:
            os.system('/afs/cs.pitt.edu/usr0/vpetrucci/move-'+APP+'.sh 2,3 >/dev/null')        

        prev_mapping = mapping

    elif policy == 'pidcontrol95':
        
        Kp = 1.5
#        Kp = 0.11        
        Ki = 0.01
        Kd = 0.01
            
        #rand_num = random.random()
        #if rand_num >= 0.99:
        #    if deadband_factor > 0.0:
        #        deadband_factor -= 0.1
        #        if deadband_factor < 0.0: deadband_factor = 0.0       
        #        print '!!!! TRYING new deadband_factor:', deadband_factor

        dt = SLEEP_INTERVAL

#        error = TARGET_DELAY*0.8 - p90th_delay
        error = (TARGET_DELAY - p95th_delay) * 100
        #if error > 0:
        #    if (error / TARGET_DELAY) <= deadband_factor:
        #        error = 0
          #  else:
           #     error = error - 

#        if error > 0:
#            if (error / TARGET_DELAY) <= pid_threshold:
#                error = 0.0

        print 'error', error
#        integral = integral + ((previous_error + error)/2.0)*dt
        integral = integral + error*dt

        if integral > output_max / Ki:
            integral = output_max / Ki
        elif integral < 0:
            integral = 0

        derivative = (error - previous_error)/dt
    
        output = Kp*error + Ki*integral + Kd*derivative
        previous_error = error
    
        if output < 0:
            output = 0
        elif output > output_max:
            output = output_max

        #print 'output', output
        
        mapping = output_mapping(output)

        app_alloc = core_config[mapping]

        # going up and it was down previously? bad!
        #if mapping > prev_mapping and went_down:
        #    if deadband_factor < 0.5:
        #        deadband_factor += 0.1       
        #        print '!!!! Setting new deadband_factor:',  deadband_factor            
        
        # going down ?
        #if mapping < prev_mapping:
        #    went_down = True
        #else:
        #    went_down = False
        
        #if mapping != prev_mapping:       
        print 'MOVING TO', app_alloc                
        if app_alloc == [0]:
            os.system('/afs/cs.pitt.edu/usr0/vpetrucci/move-'+APP+'.sh 0 >/dev/null')
        elif app_alloc == [0,1]:
            os.system('/afs/cs.pitt.edu/usr0/vpetrucci/move-'+APP+'.sh 0,1 >/dev/null')
        elif app_alloc == [2]:
            os.system('/afs/cs.pitt.edu/usr0/vpetrucci/move-'+APP+'.sh 2 >/dev/null')
        elif app_alloc == [2,3]:
            os.system('/afs/cs.pitt.edu/usr0/vpetrucci/move-'+APP+'.sh 2,3 >/dev/null')        

        prev_mapping = mapping
        
    elif policy == 'pidqoscontrol':

        Kp = 0.11
        Ki = 0.01
        Kd = 0.01
        
        dt = SLEEP_INTERVAL

        error = TARGET_DELAY - p90th_delay

        integral = integral + ((previous_error + error)/2.0)*dt

        if integral > output_max / Ki:
            integral = output_max / Ki
        elif integral < 0:
            integral = 0

        derivative = (error - previous_error)/dt
    
        output = Kp*error + Ki*integral + Kd*derivative
        previous_error = error
    
        if output < 0:
            output = 0
        elif output > output_max:
            output = output_max

        mapping = output_mapping(output)

        load_k = int(math.ceil(avg_qps))
               
        pred_qos = p90th_tab[mapping][load_k]

        # going down
        if mapping < prev_mapping:
            #print 'time', t*5, 'trying to go down, while prev_mapping', prev_mapping, 'cur_mapping', cur_mapping
            if pred_qos > TARGET_DELAY:
               # print 'time', t*5, 'but pred_qos = ', pred_qos, 'and qos_target = ', qos_target
                mapping = prev_mapping
                #print 'time', t*5, 'set cur_mapping = ', cur_mapping, 'back to', prev_mapping
            #else:
             #   print 'time', t*5, 'We are safe!'

        # no adaptation from PID
        elif mapping == prev_mapping:
            if pred_qos > TARGET_DELAY:
                for i in range(mapping+1, NUM_CORE_CONFIG):
                    if p90th_tab[i][load_k] < TARGET_DELAY or i == 3:
                        mapping = i
                        break

        app_alloc = core_config[mapping]               
    
        print 'moving to', app_alloc
        os.system('/afs/cs.pitt.edu/usr0/vpetrucci/move-'+APP+'.sh ' + app_alloc + ' >/dev/null')

        prev_mapping = mapping


    elif policy == 'pidqoscontrol95':

        Kp = 0.11
        Ki = 0.01
        Kd = 0.01
        
        dt = SLEEP_INTERVAL

        error = TARGET_DELAY - p95th_delay

        integral = integral + ((previous_error + error)/2.0)*dt

        if integral > output_max / Ki:
            integral = output_max / Ki
        elif integral < 0:
            integral = 0

        derivative = (error - previous_error)/dt
    
        output = Kp*error + Ki*integral + Kd*derivative
        previous_error = error
    
        if output < 0:
            output = 0
        elif output > output_max:
            output = output_max

        mapping = output_mapping(output)

        load_k = int(math.ceil(avg_qps))
               
        pred_qos = p95th_tab[mapping][load_k]

        # going down
        if mapping < prev_mapping:
            #print 'time', t*5, 'trying to go down, while prev_mapping', prev_mapping, 'cur_mapping', cur_mapping
            if pred_qos > TARGET_DELAY:
               # print 'time', t*5, 'but pred_qos = ', pred_qos, 'and qos_target = ', qos_target
                mapping = prev_mapping
                #print 'time', t*5, 'set cur_mapping = ', cur_mapping, 'back to', prev_mapping
            #else:
             #   print 'time', t*5, 'We are safe!'

        # no adaptation from PID
        elif mapping == prev_mapping:
            if pred_qos > TARGET_DELAY:
                for i in range(mapping+1, NUM_CORE_CONFIG):
                    if p95th_tab[i][load_k] < TARGET_DELAY or i == 3:
                        mapping = i
                        break

        app_alloc = core_config[mapping]               
    
        print 'moving to', app_alloc
        os.system('/afs/cs.pitt.edu/usr0/vpetrucci/move-'+APP+'.sh ' + app_alloc + ' >/dev/null')

        prev_mapping = mapping


    elif policy == 'reactive_swap':
        if p90th_delay > TARGET_DELAY*DELAY_UP_THR:
            print 'moving to two big cores'
            os.system('/afs/cs.pitt.edu/usr0/vpetrucci/move-'+APP+'.sh 2,3 >/dev/null')
            app_alloc = [2,3]
            
        elif p90th_delay < TARGET_DELAY*DELAY_DOWN_THR:            
            print 'moving BACK to two small cores'
            os.system('/afs/cs.pitt.edu/usr0/vpetrucci/move-'+APP+'.sh 0,1 >/dev/null')
            app_alloc = [0,1]
            
    elif policy == 'reactive_batch':

        if p95th_delay > TARGET_DELAY*DELAY_UP_THR:
            print 'Moving search to big cores...'
            os.system('/afs/cs.pitt.edu/usr0/vpetrucci/move-'+APP+'.sh 2,3 >/dev/null')
            os.system('/afs/cs.pitt.edu/usr0/vpetrucci/move-batch-jobs.sh 0,1 >/dev/null')
            app_alloc = [2, 3]
            
        elif p95th_delay < TARGET_DELAY*DELAY_DOWN_THR:
            print 'Moving search to small cores...'
            os.system('/afs/cs.pitt.edu/usr0/vpetrucci/move-batch-jobs.sh 2,3 >/dev/null')
            os.system('/afs/cs.pitt.edu/usr0/vpetrucci/move-'+APP+'.sh 0,1 >/dev/null')
            app_alloc = [0, 1]               

    elif policy == 'reactive_batch_energy':

        if p95th_delay > TARGET_DELAY*DELAY_UP_THR:
            
            b_pids = batch_pids()
            for b in b_pids:
                p = psutil.Process(b)
                p.resume()
                
            print 'Moving search to big cores...'
            os.system('/afs/cs.pitt.edu/usr0/vpetrucci/move-'+APP+'.sh 2,3 >/dev/null')
       #     os.system('/afs/cs.pitt.edu/usr0/vpetrucci/move-batch-jobs.sh 0,1 >/dev/null')
            app_alloc = [2, 3]
            
        elif p95th_delay < TARGET_DELAY*DELAY_DOWN_THR:
            
            b_pids = batch_pids()
            for b in b_pids:
                p = psutil.Process(b)
                p.suspend()
                
            print 'Moving search to small cores...'
         #   os.system('/afs/cs.pitt.edu/usr0/vpetrucci/move-batch-jobs.sh 2,3 >/dev/null')
            os.system('/afs/cs.pitt.edu/usr0/vpetrucci/move-'+APP+'.sh 0,1 >/dev/null')
            app_alloc = [0, 1]      
            
    elif policy == 'reactive_batch_corun':
        
        if p95th_delay > TARGET_DELAY*DELAY_UP_THR:
            
            b_pids = batch_pids()
            core_map = {}
            for b in b_pids:
                core_map[which_core(b)] = b
            
            #os.system('taskset -c -p 1 ' + str(b_pids[0]) + ' > /dev/null')
            print 'b_bids', b_pids
            print 'core_map', core_map
            print 'paused_jobs_per_core', paused_jobs_per_core

            if app_alloc == [0]:
                app_alloc = [0,1]
                print 'moving to two small cores'
                pid_to_suspend = core_map[1]
                print 'suspending pid', pid_to_suspend 
                p = psutil.Process(pid_to_suspend)
                p.suspend()
                paused_jobs_per_core[1] = pid_to_suspend
                os.system('/afs/cs.pitt.edu/usr0/vpetrucci/move-'+APP+'.sh 0,1 >/dev/null')
                
            elif app_alloc == [0,1]:
                app_alloc = [2]
                print 'moving to one big core'
                pid_to_resume = paused_jobs_per_core[1]
                print 'resuming pid', pid_to_suspend 
                p = psutil.Process(pid_to_resume)
                p.resume()  
                pid_to_move = core_map[2]
                os.system('taskset -c -p 0 ' + str(pid_to_move) + ' > /dev/null')
                os.system('taskset -c -p 0 ' + str(get_ppid(pid_to_move))+ ' > /dev/null')
                os.system('/afs/cs.pitt.edu/usr0/vpetrucci/move-'+APP+'.sh 2 >/dev/null')
                
            elif app_alloc == [2]:
                app_alloc = [2,3]
                print 'moving to two big cores'  
                pid_to_suspend = core_map[4]
                print 'suspending pid', pid_to_suspend 
                p = psutil.Process(pid_to_suspend)
                p.suspend()
                paused_jobs_per_core[4] = pid_to_suspend
                os.system('/afs/cs.pitt.edu/usr0/vpetrucci/move-'+APP+'.sh 2,3 >/dev/null')
                
        elif p95th_delay < TARGET_DELAY*DELAY_DOWN_THR:

            print 'b_bids', b_pids
            print 'core_map', core_map
            print 'paused_jobs_per_core', paused_jobs_per_core
            
            b_pids = batch_pids()
            core_map = {}
            for b in b_pids:
                core_map[which_core(b)] = b
                
            if app_alloc == [0,1]:
                app_alloc = [0]
                print 'moving BACK to one small core'
                pid_to_resume = paused_jobs_per_core[1]
                print 'resuming pid', pid_to_suspend 
                p = psutil.Process(pid_to_resume)
                p.resume()  
                os.system('/afs/cs.pitt.edu/usr0/vpetrucci/move-'+APP+'.sh 0 >/dev/null')
                
            elif app_alloc == [2]:
                app_alloc = [0,1]  
                print 'moving BACK to two small cores'
                pid_to_suspend = core_map[1]
                print 'suspending pid', pid_to_suspend 
                p = psutil.Process(pid_to_suspend)
                p.suspend()
                paused_jobs_per_core[1] = pid_to_suspend
                pid_to_move = core_map[0]
                os.system('taskset -c -p 2 ' + str(pid_to_move) + ' > /dev/null')
                os.system('taskset -c -p 2 ' + str(get_ppid(pid_to_move))+ ' > /dev/null')
                os.system('/afs/cs.pitt.edu/usr0/vpetrucci/move-'+APP+'.sh 0,1 >/dev/null')
                
            elif app_alloc == [2,3]:
                app_alloc = [2]
                print 'moving BACK to one big core'   
                pid_to_resume = paused_jobs_per_core[4]
                print 'resuming pid', pid_to_suspend 
                p = psutil.Process(pid_to_resume)
                p.resume()                  
                os.system('/afs/cs.pitt.edu/usr0/vpetrucci/move-'+APP+'.sh 2 >/dev/null')

    elif policy == 'reactive_batch_corun_energy':

        if p95th_delay > TARGET_DELAY*DELAY_UP_THR:
            
            if app_alloc == [0]:
                os.system('/afs/cs.pitt.edu/usr0/vpetrucci/move-'+APP+'.sh 0,1 >/dev/null')
                app_alloc = [0,1]
                print 'moving to two small cores'
            
                b_pids = batch_pids()
                for b in b_pids:
                    p = psutil.Process(b)
                    p.suspend()
                
            elif app_alloc == [0,1]:
                os.system('/afs/cs.pitt.edu/usr0/vpetrucci/move-'+APP+'.sh 2 >/dev/null')
                app_alloc = [2]
                print 'moving to one big core'
                  
                b_pids = batch_pids()
                for b in b_pids:
                    p = psutil.Process(b)
                    p.resume()

            elif app_alloc == [2]:
                os.system('/afs/cs.pitt.edu/usr0/vpetrucci/move-'+APP+'.sh 2,3 >/dev/null')
                app_alloc = [2,3]
                print 'moving to two big cores'
            
                    
        elif p95th_delay < TARGET_DELAY*DELAY_DOWN_THR:
            
            if app_alloc == [0,1]:
                os.system('/afs/cs.pitt.edu/usr0/vpetrucci/move-'+APP+'.sh 0 >/dev/null')
                app_alloc = [0]
                print 'moving BACK to one small core'

                b_pids = batch_pids()
                if len(b_pids) != 2:
                    print 'OPS error... b_pids diff 2 !!!'
                else:
             #       jobs_paused += [b_pids[0]]
                    p = psutil.Process(b_pids[0])
                    p.suspend()                     
                
            elif app_alloc == [2]:
                os.system('/afs/cs.pitt.edu/usr0/vpetrucci/move-'+APP+'.sh 0,1 >/dev/null')
                app_alloc = [0,1]  
                print 'moving BACK to two small cores'
                
                b_pids = batch_pids()
                for b in b_pids:
                    p = psutil.Process(b)
                    p.suspend()
                    
            elif app_alloc == [2,3]:
                os.system('/afs/cs.pitt.edu/usr0/vpetrucci/move-'+APP+'.sh 2 >/dev/null')
                app_alloc = [2]
                print 'moving BACK to one big core'                            
                

    elif policy == 'reactive_batch_corun_smart':
        pass
        
    keep_running = int(open('/ramcache/mapper_running').read())
    if not keep_running: break
        
    t2 = time.time()
    
    to_sleep = SLEEP_INTERVAL - (t2-t1)
    cpu_util = psutil.cpu_percent(to_sleep, percpu=True)
    #cpu_util = psutil.cpu_percent(to_sleep, percpu=True)
    #time.sleep(to_sleep)

mon_file.close()

tail_running = False

time.sleep(2)

print 'cya!!'



