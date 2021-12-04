
import os
from scipy import stats
import re

def read_values():
    
    avg_qps = 0.0
    avg_delay = 0.0
    p90th_delay = 0.0
    p95th_delay = 0.0
    p99th_delay = 0.0
    
    workload = {}
    workload['QPS'] = []
    lines = os.popen('tail -n 100 /ramcache/cassandra-client.txt | grep READ').read().split('\n')[:-1]
    if len(lines) < 5:
        return avg_qps, avg_delay, p90th_delay, p95th_delay, p99th_delay
                
    for l in list(reversed(lines)):
        
        qps = re.search("([0-9.]*) current", l).groups()[0]        
        workload['QPS'] += [float(qps)]
        
        for oper_lat in re.findall("\[([^]]*)\]", l):
            name = oper_lat.split(' ')[0]
            val = float(oper_lat.split('=')[1])
            
            if name not in workload: workload[name] = [val]
            workload[name] += [val]

    qps_lines = workload['QPS']
    lat_lines = workload['READ']
    if len(lat_lines) < 5 or len(qps_lines) < 5:
        return avg_qps, avg_delay, p95th_delay, p99th_delay

    avg_qps = sum(qps_lines) / len(qps_lines)
    avg_delay = (sum(lat_lines) / len(lat_lines)) / 1000.0

    p95th_delay = stats.scoreatpercentile(lat_lines, 95) / 1000.0
    p99th_delay = stats.scoreatpercentile(lat_lines, 99) / 1000.0

    return avg_qps, avg_delay, p95th_delay, p99th_delay
