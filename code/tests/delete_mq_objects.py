'''
Created on 17 Nov 2010

This script creates the MQ objects required for the test suite.

@author: hannes
'''

import subprocess
import sys
import time


mqsc_script = """
DEFINE LISTENER(TEST.LISTENER) TRPTYPE(TCP) PORT(31414) CONTROL(QMGR) REPLACE
START LISTENER(TEST.LISTENER)
DEFINE QL(RFH2.TEST) REPLACE
"""

print "Creating all MQ Objects required to run the test.\n"

print "Checking if Queue Manager QM01 exists.\n"
dspmq_proc = subprocess.Popen(["dspmq", "-mQM01"], stdout=subprocess.PIPE,
                              stderr=subprocess.PIPE)
dspmq_output, dspmq_error = dspmq_proc.communicate()

if dspmq_proc.returncode == 72:
    print "Queue manager QM01 does not exist.  Nothing to do. Exiting.\n"
    sys.exit(0)
else:
    if dspmq_proc.returncode != 0:
        print "Error Occurred\n"
        print "-" * len(dspmq_error) + "\n"
        print dspmq_error
        print "-" * len(dspmq_error) + "\n"
        print "Failed to setup MQ Environment!\n"
        sys.exit(1)

print "Stopping Queue Manager.\n"
endmqm_proc = subprocess.Popen(["endmqm", "QM01"], stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)
endmqm_output, endmqm_error = endmqm_proc.communicate()
print endmqm_error
start = time.time()
time_up = 60 - (time.time() - start)
current_disp = start
disp_time = 5 - (time.time() - current_disp)
done = False
while not done:
    if time_up <= 0:
        done = True
    if dspmq_output.count("STATUS(Ended"):
        done = True
    if disp_time <= 0:
        print dspmq_output
        current_disp = time.time()
    dspmq_proc = subprocess.Popen(["dspmq", "-mQM01"],
                                  stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE)
    dspmq_output, dspmq_error = dspmq_proc.communicate()
    time_up = 60 - (time.time() - start)
    times = 0
    disp_time = 5 - (time.time() - current_disp)

if time_up <= 0:
    print "Could not end Queue Manager.You can try running the script again.\n"
    print "-" * 80 + "\n"
    print endmqm_proc.communicate()[1]
    print "-" * 80 + "\n"
    sys.exit(0)

print "Queue Manager Stopped.\n"


time.sleep(5)
dltmqm_proc = subprocess.Popen(["dltmqm", "QM01"], stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)
dltmqm_output, dltmqm_error = dltmqm_proc.communicate()

if dltmqm_proc.returncode != 0:
    print "Error while deleting Queue Manager QM01."
    print "-" * 80 + "\n"
    print dltmqm_error
    print "-" * 80 + "\n"
    print "MQ Environment not deleted."
    sys.exit(1)

print "Queue Manager Deleted."
print "-" * 80 + "\n"
print dltmqm_error
print "-" * 80 + "\n"

print "MQ Environment Deleted.\n"
