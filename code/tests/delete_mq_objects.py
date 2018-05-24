"""
Created on 17 Nov 2010

This script creates the MQ objects required for the test suite.

@author: hannes
"""

import subprocess
import sys
import time
import config

print("Deleting all MQ Objects required to run the test.\n")

print("Checking if Queue Manager %s exists.\n" % config.MQ.QM.NAME)
dspmq_proc = subprocess.Popen(
    ["dspmq", "-m%s" % config.MQ.QM.NAME], stdout=subprocess.PIPE,
    stderr=subprocess.PIPE)
dspmq_output, dspmq_error = dspmq_proc.communicate()

if dspmq_proc.returncode == 72:
    print("Queue manager %s does not exist.  Nothing to do. Exiting.\n" % config.MQ.QM.NAME)
    sys.exit(0)
else:
    if dspmq_proc.returncode != 0:
        print("Error Occurred\n")
        print("-" * len(dspmq_error) + "\n")
        print(dspmq_error)
        print("-" * len(dspmq_error) + "\n")
        print("Failed to setup MQ Environment!\n")
        sys.exit(1)

print("Stopping Queue Manager.\n")
endmqm_proc = subprocess.Popen(
    ["endmqm", config.MQ.QM.NAME], stdout=subprocess.PIPE,
    stderr=subprocess.PIPE)
endmqm_output, endmqm_error = endmqm_proc.communicate()
print(endmqm_error)
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
        print(dspmq_output)
        current_disp = time.time()
    dspmq_proc = subprocess.Popen(["dspmq", "-m%s" % config.MQ.QM.NAME],
                                  stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE)
    dspmq_output, dspmq_error = dspmq_proc.communicate()
    time_up = 60 - (time.time() - start)
    times = 0
    disp_time = 5 - (time.time() - current_disp)

if time_up <= 0:
    print("Could not end Queue Manager.You can try running the script again.\n")
    print("-" * 80 + "\n")
    print(endmqm_proc.communicate()[1])
    print("-" * 80 + "\n")
    sys.exit(0)

print("Queue Manager Stopped.\n")


time.sleep(5)
dltmqm_proc = subprocess.Popen(["dltmqm", config.MQ.QM.NAME],
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)
dltmqm_output, dltmqm_error = dltmqm_proc.communicate()

if dltmqm_proc.returncode != 0:
    print("Error while deleting Queue Manager %s." % config.MQ.QM.NAME)
    print("-" * 80 + "\n")
    print(dltmqm_error)
    print("-" * 80 + "\n")
    print("MQ Environment not deleted.")
    sys.exit(1)

print("Queue Manager Deleted.")
print("-" * 80 + "\n")
print(dltmqm_error)
print("-" * 80 + "\n")

print("MQ Environment Deleted.\n")
