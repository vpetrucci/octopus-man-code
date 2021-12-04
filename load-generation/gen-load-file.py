
import sys

#max_load = 92
max_load = float(sys.argv[1])

for l in open('google-trace.txt'):
#for l in open('google-trace-sub.txt'):
#    print int((float(l)/100.0)*max_load), 
    #print int((float(l)/100.0)*max_load), 
    print int((float(l)/100.0)*max_load), 

print ''

for l in open('google-trace.txt'):
#for l in open('google-trace-sub.txt'):
  #  print '150'+','+str(int((float(l)/100.0)*max_load))
    #print '300'+','+str(int((float(l)/100.0)*max_load))
    #print '60'+','+str(int((float(l)/100.0)*max_load))
    print '60'+','+str(int((float(l)/100.0)*max_load))

#print 48*60
