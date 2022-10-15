from multiprocessing import Pool
import time
import subprocess
import sys
import numpy as np

def f(x):
    # make some giant arrays and then do simple math on them to exercise memory
    a = np.full((20000,20000),x)
    while True:
        a = a + 1

# start the processes
#p = Pool(processes=4)
#p.map_async(f, (1.5,2.7, 3.3, 4.9))

# get their PIDs from the os
# this control script will also come up
# but it is always the last one in the list on my system
pids_bytes = subprocess.check_output(["pidof", "stress"])
pids = pids_bytes.split()
#pids.pop(-1)

# set the run time from the command line, which will be in seconds
end = 610
if len(sys.argv)>1:
    end = int(sys.argv[1])

# half period, in seconds
i=30
# state tracker
ion=True
# start time in seconds
startTime = time.time()
endTime = startTime + end

# the main loop
# sleep for 1 second, then
# check if the count of seconds since start y/ (i,j) is even or odd
# for example: y=13 => y/i = 2, y/j = 1
# we don't need the remainder, so integer division is perfect
# if even, turn the processes associated with i,j on
# if odd, turn the processes associated with i,j off
# 19 is SIGSTOP, 18 is SIGCONT
# 15 is SIGTERM
while (time.time() < endTime):
    nowTime = time.time()
    secondsSinceStart = nowTime - startTime
    if ((int(secondsSinceStart/i) % 2) == 1):
         if ion==False:
            for pid in pids:
                subprocess.call(["kill", "-s", "18", pid])
            ion=True
#            print(secondsSinceStart)
    else:
        if ion==True:
            for pid in pids:
                subprocess.call(["kill", "-s", "19", pid])
            ion=False
#            print(secondsSinceStart)
    time.sleep(0.1)

for pid in pids:
    subprocess.call(["kill", "-s", "15", pid])
#p.terminate()
