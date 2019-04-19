"""
Created on 17 Nov 2010

This script creates the MQ objects required for the test suite.

@author: hannes
"""

import subprocess
import sys
import time
import config


LINE = "-" * 80 + "\n"


# channel and tcp listener creation commands
mqsc_script_channel_listener = """
DEFINE CHL(%(channel)s) CHLTYPE(SVRCONN)
DEFINE LISTENER(TCP.LISTENER.1) TRPTYPE(TCP) PORT(%(port)s) CONTROL(QMGR) REPLACE
START LISTENER(TCP.LISTENER.1)
""" % {
    'channel': config.MQ.QM.CHANNEL,
    'port': config.MQ.QM.PORT,
    } + '\n'.join(["DEFINE QL(%s) REPLACE" % qname
                   for qname in config.MQ.QUEUE.QUEUE_NAMES.values()])


# user/password connection authentication setup (MQ>=8.0 only) 
# CHK*(OPTIONAL): If a user ID and password are provided by a client
# application then they must be a valid pair. It is not mandatory to provide
# user + password, though.
# This setting allows for testing against both MQ>=8.0 servers as well as older
# MQ versions with same test codebase.
mqsc_script_conn_auth_use_pw = """
ALTER QMGR CONNAUTH(USE.PW)
DEFINE AUTHINFO(USE.PW) AUTHTYPE(IDPWOS) FAILDLAY(%(faildlay)s) CHCKLOCL(OPTIONAL) CHCKCLNT(%(chckclnt)s)
REFRESH SECURITY TYPE(CONNAUTH)
""" % {
    'chckclnt': config.MQ.QM.CONN_AUTH.USE_PW,
    'faildlay': config.MQ.QM.CONN_AUTH.FAIL_DELAY,
    }


mqsc_script_no_conn_auth = """
ALTER QMGR CONNAUTH(' ')
REFRESH SECURITY TYPE(CONNAUTH)
"""


# Disable channel auth records feature.
# WARNING: Admin client connections will now be accepted per default - use for
# testing purposes only!
mqsc_script_channel_auth = """
ALTER QMGR CHLAUTH(DISABLED)
"""


def run_mqsc(mqsc_script, errormsg="MQSC commands not successful",
             verbose=True):
    """Helper function to run MQSC commands.

    Returns a (returncode, stdout, stderr)-tuple of the command script.
    """
    mqsc_script = mqsc_script.encode('ascii')
    if verbose:
        print("runmqsc:")
        print(mqsc_script.replace(b'\n', b'\n    '))
    runmqsc_proc = subprocess.Popen(
        ["runmqsc", config.MQ.QM.NAME], stdout=subprocess.PIPE,
        stdin=subprocess.PIPE, stderr=subprocess.PIPE)
    runmqsc_output, runmqsc_error = runmqsc_proc.communicate(mqsc_script)
    print(LINE)
    print(runmqsc_output)
    print(LINE)
    if runmqsc_proc.returncode not in (0, 10):
        print(errormsg)
        print(LINE)
        print(runmqsc_error)
        print(LINE)
    return runmqsc_proc.returncode, runmqsc_output, runmqsc_error


print("Creating all MQ Objects required to run the test.\n")

print("Checking if Queue Manager %s exists.\n" % config.MQ.QM.NAME)
dspmq_proc = subprocess.Popen(
    ["dspmq", "-m%s" % config.MQ.QM.NAME], stdout=subprocess.PIPE,
    stderr=subprocess.PIPE)
dspmq_output, dspmq_error = dspmq_proc.communicate()

if dspmq_proc.returncode == 72:
    print("Queue manager %s does not exist.  Attempting to create.\n" % config.MQ.QM.NAME)
    crtmqm_proc = subprocess.Popen(["crtmqm", config.MQ.QM.NAME],
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)
    crtmqm_output, crtmqm_error = crtmqm_proc.communicate()
    if crtmqm_proc.returncode != 0:
        print("Error Occured while creating Queue Manager %s.\n" % config.MQ.QM.NAME)
        print("-" * len(crtmqm_error) + "\n")
        print(crtmqm_error)
        print("-" * len(crtmqm_error) + "\n")
        print("Failed to setup MQ Enviromment!\n")
        sys.exit(1)
    print("Queue manager %s created.\n" % config.MQ.QM.NAME)
else:
    if dspmq_proc.returncode == 0:
        print("Queue Manager %s exists.\n" % config.MQ.QM.NAME)
        print("-" * len(dspmq_output) + "\n")
        print(dspmq_output)
        print("-" * len(dspmq_output) + "\n")
    else:
        print("Error Occured\n")
        print("-" * len(dspmq_error) + "\n")
        print(dspmq_error)
        print("-" * len(dspmq_error) + "\n")
        print("Failed to setup MQ Enviromment!\n")
        sys.exit(1)

strmqm_proc = subprocess.Popen(
    ["strmqm", config.MQ.QM.NAME], stdout=subprocess.PIPE,
    stderr=subprocess.PIPE)
strmqm_output, strmqm_error = strmqm_proc.communicate()

if strmqm_proc.returncode == 5:
    print(strmqm_error)
else:
    if strmqm_proc.returncode != 0:
        print("Error.  Could not start Queue Manager.")
        print("-" * len(strmqm_error) + "\n")
        print(strmqm_error)
        print("-" * len(strmqm_error) + "\n")
        sys.exit(1)

time.sleep(2)

print("Creating MQ channel and listener Objects.")
run_mqsc(mqsc_script_channel_listener,
         errormsg="MQ channel and listener objects creation not successful.")

if config.MQ.QM.CONN_AUTH.SUPPORTED == '1':
    print("Setting up MQ queue manager user/password connection authentication.")
    run_mqsc(mqsc_script_conn_auth_use_pw,
             errormsg="MQ queue manager connection authentication setup not successful.")
else:
    if int(config.MQ.QM.MIN_COMMAND_LEVEL) >= 800:
        print("Switching off MQ queue manager connection authentication.")
        run_mqsc(mqsc_script_no_conn_auth,
                 errormsg="MQ queue manager connection authentication setup not successful.")
    else:
        print("Connection authentication not applicable for pre-8.0 MQ.")
        
    
print("Disabling MQ queue manager channel authentication records feature.")
run_mqsc(mqsc_script_channel_auth,
         errormsg="Disabling MQ queue manager channel authentication records not successful.")


print("MQ Environment Created.  Ready for tests.\n")
