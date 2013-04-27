# See discussion and more examples at http://packages.python.org/pymqi/examples.html
# or in doc/sphinx/examples.rst in the source distribution.

import logging

import pymqi
import CMQC, CMQCFC, CMQXC

logging.basicConfig(level=logging.INFO)

queue_manager = "QM01"
channel = "CHANNEL.1"
host = "127.0.0.1"
port = "1434"
conn_info = "%s(%s)" % (host, port)

prefix = "SYSTEM.*"
queue_type = CMQC.MQQT_MODEL

args = {CMQC.MQCA_Q_NAME: prefix,
        CMQC.MQIA_Q_TYPE: queue_type}

qmgr = pymqi.connect(queue_manager, channel, conn_info)
pcf = pymqi.PCFExecute(qmgr)

try:
    response = pcf.MQCMD_INQUIRE_Q(args)
except pymqi.MQMIError, e:
    if e.comp == CMQC.MQCC_FAILED and e.reason == CMQC.MQRC_UNKNOWN_OBJECT_NAME:
        logging.info("No queues matched given arguments.")
    else:
        raise
else:
    for queue_info in response:
        queue_name = queue_info[CMQC.MQCA_Q_NAME]
        logging.info("Found queue [%s]" % queue_name)

qmgr.disconnect()
