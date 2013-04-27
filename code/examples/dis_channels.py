# See discussion and more examples at http://packages.python.org/pymqi/examples.html
# or in doc/sphinx/examples.rst in the source distribution.

import logging

import pymqi
import CMQC, CMQCFC

logging.basicConfig(level=logging.INFO)

queue_manager = "QM01"
channel = "SVRCONN.1"
host = "192.168.1.135"
port = "1434"
conn_info = "%s(%s)" % (host, port)

prefix = "SYSTEM.*"

args = {CMQCFC.MQCACH_CHANNEL_NAME: prefix}

qmgr = pymqi.connect(queue_manager, channel, conn_info)
pcf = pymqi.PCFExecute(qmgr)

try:
    response = pcf.MQCMD_INQUIRE_CHANNEL(args)
except pymqi.MQMIError, e:
    if e.comp == CMQC.MQCC_FAILED and e.reason == CMQC.MQRC_UNKNOWN_OBJECT_NAME:
        logging.info("No channels matched prefix [%s]" % prefix)
    else:
        raise
else:
    for channel_info in response:
        channel_name = channel_info[CMQCFC.MQCACH_CHANNEL_NAME]
        logging.info("Found channel [%s]" % channel_name)

qmgr.disconnect()
