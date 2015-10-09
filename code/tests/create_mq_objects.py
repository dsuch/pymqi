'''
Created on 17 Nov 2010

This script creates the MQ objects required for the test suite.

@author: hannes
'''

import subprocess
import sys
import time
import config


mqsc_script = """
DEFINE CHL(%(channel)s) CHLTYPE(SVRCONN)
DEFINE LISTENER(TCP.LISTENER.1) TRPTYPE(TCP) PORT(%(port)s) CONTROL(QMGR) REPLACE
START LISTENER(TCP.LISTENER.1)
""" % {
    'channel': config.MQ.QM.CHANNEL,
    'port': config.MQ.QM.PORT,
    } + '\n'.join([ "DEFINE QL(%s) REPLACE" % qname 
                    for qname in config.MQ.QUEUE.QUEUE_NAMES.values() ])


print "Creating all MQ Objects required to run the test.\n"

print "Checking if Queue Manager %s exists.\n" % config.MQ.QM.NAME
dspmq_proc = subprocess.Popen(
    ["dspmq", "-m%s" % config.MQ.QM.NAME], stdout=subprocess.PIPE,
    stderr=subprocess.PIPE)
dspmq_output, dspmq_error = dspmq_proc.communicate()

if dspmq_proc.returncode == 72:
    print ("Queue manager %s does not exist.  Attempting to create.\n" %
           config.MQ.QM.NAME)
    crtmqm_proc = subprocess.Popen(["crtmqm", config.MQ.QM.NAME],
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)
    crtmqm_output, crtmqm_error = crtmqm_proc.communicate()
    if crtmqm_proc.returncode != 0:
        print ("Error Occured while creating Queue Manager %s.\n" %
               config.MQ.QM.NAME)
        print "-" * len(crtmqm_error) + "\n"
        print crtmqm_error
        print "-" * len(crtmqm_error) + "\n"
        print "Failed to setup MQ Enviromment!\n"
        sys.exit(1)
    print "Queue manager %s created.\n" % config.MQ.QM.NAME
else:
    if dspmq_proc.returncode == 0:
        print "Queue Manager %s exists.\n" % config.MQ.QM.NAME
        print "-" * len(dspmq_output) + "\n"
        print dspmq_output
        print "-" * len(dspmq_output) + "\n"
    else:
        print "Error Occured\n"
        print "-" * len(dspmq_error) + "\n"
        print dspmq_error
        print "-" * len(dspmq_error) + "\n"
        print "Failed to setup MQ Enviromment!\n"
        sys.exit(1)

strmqm_proc = subprocess.Popen(
    ["strmqm", config.MQ.QM.NAME], stdout=subprocess.PIPE,
    stderr=subprocess.PIPE)
strmqm_output, strmqm_error = strmqm_proc.communicate()

if strmqm_proc.returncode == 5:
    print strmqm_error
else:
    if strmqm_proc.returncode != 0:
        print "Error.  Could not start Queue Manager."
        print "-" * len(strmqm_error) + "\n"
        print strmqm_error
        print "-" * len(strmqm_error) + "\n"
        sys.exit(1)

time.sleep(2)

print "Creating MQ Objects."
runmqsc_proc = subprocess.Popen(["runmqsc", config.MQ.QM.NAME],
                                stdout=subprocess.PIPE, stdin=subprocess.PIPE,
                                stderr=subprocess.PIPE)
runmqsc_output, runmqsc_error = runmqsc_proc.communicate(mqsc_script)
print "-" * 80 + "\n"
print runmqsc_output
print "-" * 80 + "\n"
if runmqsc_proc.returncode not in (0, 10):
    print "Creation of MQ Objects not successful."
    print "-" * 80 + "\n"
    print runmqsc_error
    print "-" * 80 + "\n"

print "MQ Environment Created.  Ready for tests.\n"
