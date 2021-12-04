
import os
from scipy import stats

def read_values():

    tab_log = {}
    cur_date = os.popen('date +%Y-%m-%d').read().strip()
    web_lines=os.popen('tail -n 1000 /ramcache/logs/localhost_access_log.'+cur_date+'.txt').read().split('\n')[:-1]
    avg_delay_list = []
    for l in reversed(web_lines):
        # format: 136.142.50.220 - - 1368662334 "GET /en/ HTTP/1.0" 200 4869 12
        try:
            tstamp = int(l.split('"')[0].split(' ')[3])
            delay = float(l.split('"')[2].split(' ')[3])
            if tstamp not in tab_log: tab_log[tstamp] = []
            tab_log[tstamp] += [delay]
            avg_delay_list += [delay]
        except:
        #    print 'ops look at line from web log:', l
            continue
        if len(tab_log) >= 10:
         #   print 'tab_lob has size:', len(tab_log)
            break

    avg_qps_list = []     
    for val in tab_log.values():
       avg_qps_list += [len(val)]
#       avg_delay_list += val
          
    if len(avg_qps_list) > 0:
        avg_qps = sum(avg_qps_list) / float(len(avg_qps_list))    
    else:
        avg_qps = 0.0

    if len(avg_delay_list) > 0:
        avg_delay = sum(avg_delay_list) / float(len(avg_delay_list))   
    else:
        avg_delay = 0.0  

    if len(avg_delay_list) > 0:
        p90th_delay = stats.scoreatpercentile(avg_delay_list, 90)
        p95th_delay = stats.scoreatpercentile(avg_delay_list, 95)
        p99th_delay = stats.scoreatpercentile(avg_delay_list, 99)        
    else:
        p90th_delay = 0.0
        p95th_delay = 0.0
        p99th_delay = 0.0
        
    return avg_qps, avg_delay, p90th_delay, p95th_delay, p99th_delay
        

