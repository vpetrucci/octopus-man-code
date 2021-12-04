import os
import subprocess
import time
import signal
import sys

BASE_PATH="/afs/cs.pitt.edu/usr0/vpetrucci/disk1"
SPEC_PATH=BASE_PATH+"/cpu2006/benchspec/CPU2006/"
RUN_PATH="/run/run_base_ref_amd64-m64-gcc42-nn.000"

EXE_SUFIX="_base.amd64-m64-gcc42-nn"

cmd_list = {'soplex': ('450.soplex/exe/soplex'+EXE_SUFIX +' -m3500 ref.mps ', '450.soplex'+RUN_PATH),
            'gamess': ("416.gamess/exe/gamess"+EXE_SUFIX +'  < h2ocu2+.gradient.config ', '416.gamess'+RUN_PATH),
            'milc': ('433.milc/exe/milc'+EXE_SUFIX +' < su3imp.in ', '433.milc'+RUN_PATH),
            'zeusmp':('434.zeusmp/exe/zeusmp'+EXE_SUFIX +' ', '434.zeusmp'+RUN_PATH),
            'astar':('473.astar/exe/astar'+EXE_SUFIX +' BigLakes2048.cfg ', '473.astar'+RUN_PATH),
            'calculix':('454.calculix/exe/calculix'+EXE_SUFIX +' -i  hyperviscoplastic', '454.calculix'+RUN_PATH),
             'lbm':('470.lbm/exe/lbm'+EXE_SUFIX +' 3000 reference.dat 0 0 100_100_130_ldc.of ', '470.lbm'+RUN_PATH),
            'bwaves':('410.bwaves/exe/bwaves'+EXE_SUFIX +' ', '410.bwaves'+RUN_PATH),
            'gobmk':('445.gobmk/exe/gobmk'+EXE_SUFIX +' --quiet --mode gtp < nngs.tst ', '445.gobmk'+RUN_PATH),
            'leslie3d': ('437.leslie3d/exe/leslie3d'+EXE_SUFIX +' < leslie3d.in ', '437.leslie3d'+RUN_PATH),
            'bzip2':('401.bzip2/exe/bzip2'+EXE_SUFIX +' input.source 280 ', '401.bzip2'+RUN_PATH),
            'cactusADM':('436.cactusADM/exe/cactusADM'+EXE_SUFIX +' benchADM.par ', '436.cactusADM'+RUN_PATH),
            'mcf':('429.mcf/exe/mcf'+EXE_SUFIX +' inp.in ', '429.mcf'+RUN_PATH),
            'wrf':('481.wrf/exe/wrf'+EXE_SUFIX +' ', '481.wrf'+RUN_PATH),
            'hmmer':('456.hmmer/exe/hmmer'+EXE_SUFIX +' --fixed 0 --mean 500 --num 500000 --sd 350 --seed 0 retro.hmm > /dev/null', '456.hmmer'+RUN_PATH),
            'namd':('444.namd/exe/namd'+EXE_SUFIX +' --input namd.input --iterations 38 --output /dev/null', '444.namd'+RUN_PATH),
            'GemsFDTD':('459.GemsFDTD/exe/GemsFDTD'+EXE_SUFIX +' ', '459.GemsFDTD'+RUN_PATH),
            'sjeng':('458.sjeng/exe/sjeng'+EXE_SUFIX +' ref.txt', '458.sjeng'+RUN_PATH),
            'dealII':('447.dealII/exe/sjeng'+EXE_SUFIX +' 23 ', '447.dealII'+RUN_PATH),
            'omnetpp':('471.omnetpp/exe/omnetpp'+EXE_SUFIX +' omnetpp.ini ', '471.omnetpp'+RUN_PATH),
            'povray': ('453.povray/exe/povray'+EXE_SUFIX +' SPEC-benchmark-ref.ini ', '453.povray'+RUN_PATH),
            'gromacs': ('435.gromacs/exe/gromacs'+EXE_SUFIX +' -silent -deffnm gromacs -nice 0 ', '435.gromacs'+RUN_PATH),
            'libquantum': ('462.libquantum/exe/libquantum'+EXE_SUFIX +' 1397 8 ', '462.libquantum'+RUN_PATH),
            'tonto':('465.tonto/exe/tonto'+EXE_SUFIX +' ', '465.tonto'+RUN_PATH)}

def get_children(pid):
    return [int(i) for i in os.popen('ps -o pid --no-headers --ppid '+str(pid)).read().split('\n')[:-1]]

def find_task(ppid):
    c = get_children(ppid)
    if c == []:
        return ppid
    p = c[0]
    while c:
        c = get_children(p)
        if c:
            p = c[0]
    return p

def run_apps(app, i):
    procs = {}
    task_procs = {}
    
  #  for i in range(copies):
  
    print 'starting', (app,i)
    os.chdir(SPEC_PATH + cmd_list[app][1]+str(i))
    cmd = SPEC_PATH + cmd_list[app][0]

    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, preexec_fn=os.setsid)
    time.sleep(1)
    procs[(app,i)] = p.pid
    task_procs[(app,i)] = find_task(p.pid)

    return procs, task_procs

app = sys.argv[1]
copies = int(sys.argv[2])

procs, task_procs = run_apps(app, copies)

while True:
  ret_pid, status, rusage = os.wait3(0)
#  print 'ret_pid', ret_pid
  (app,i) = [k for k, v in procs.iteritems() if v == ret_pid][0]
  pid = task_procs[(app,i)]

  print 'pid', pid, 'finished'
#  print 'rusage', rusage

  print 'restarting', (app,i)
  os.chdir(SPEC_PATH + cmd_list[app][1]+str(i))
  cmd = SPEC_PATH + cmd_list[app][0]
  p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, preexec_fn=os.setsid)
  time.sleep(1)
  procs[(app,i)] = p.pid
  task_procs[(app,i)] = find_task(p.pid)
  
  
  


