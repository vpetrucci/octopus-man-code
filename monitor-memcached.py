
import os
from scipy import stats
import re

def read_values():

    avg_qps = 0.0
    avg_delay = 0.0
    p90th_delay = 0.0
    p95th_delay = 0.0
    p99th_delay = 0.0
    
    tab_log = {}
    try:
        lines = open('/ramcache/loader-memcached.txt').read().strip()
        if lines == '':
            return avg_qps, avg_delay, p90th_delay, p95th_delay, p99th_delay
    except IOError:
        return avg_qps, avg_delay, p90th_delay, p95th_delay, p99th_delay
        
    try:
        d=os.popen('tail -n 20 /ramcache/loader-memcached.txt | grep -A1 avg_lat | grep -v avg_lat | grep -v "\-na" | cut -f8 -d,').read()
        lat_lines = [float(i) for i in re.findall('([0-9.]+)', d)]

        d=os.popen('tail -n 20 /ramcache/loader-memcached.txt | grep -A1 rps | grep -v rps | grep -v "\-na" | cut -f2 -d,').read()
        qps_lines = [float(i) for i in re.findall('([0-9.]+)', d)]

        d=os.popen('tail -n 20 /ramcache/loader-memcached.txt | grep -A1 95th | grep -v 95th | grep -v "\-na" | cut -f10 -d,').read()
        p95th_lines = [float(i) for i in re.findall('([0-9.]+)', d)]

        d=os.popen('tail -n 20 /ramcache/loader-memcached.txt | grep -A1 90th | grep -v 90th | grep -v "\-na" | cut -f9 -d,').read()
        p90th_lines = [float(i) for i in re.findall('([0-9.]+)', d)]
    
        d=os.popen('tail -n 20 /ramcache/loader-memcached.txt | grep -A1 99th | grep -v 99th | grep -v "\-na" | cut -f11 -d,').read()
        p99th_lines = [float(i) for i in re.findall('([0-9.]+)', d)]
    except:
        print 'tail probs..'
        return avg_qps, avg_delay, p90th_delay, p95th_delay, p99th_delay
    
    return qps_lines[-1], lat_lines[-1]/1000.0, p90th_lines[-1]/1000.0, p95th_lines[-1]/1000.0, p99th_lines[-1]/1000.0
