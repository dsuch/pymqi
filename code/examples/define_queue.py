# See discussion and more examples at http://packages.python.org/pymqi/examples.html
# or in doc/sphinx/examples.rst in the source distribution.

import pymqi
import CMQC

queue_manager = "QM01"
channel = "SVRCONN.1"
host = "192.168.1.135"
port = "1434"
conn_info = "%s(%s)" % (host, port)

queue_name = "MYQUEUE.1"
queue_type = CMQC.MQQT_LOCAL
max_depth = 123456

args = {CMQC.MQCA_Q_NAME: queue_name,
        CMQC.MQIA_Q_TYPE: queue_type,
        CMQC.MQIA_MAX_Q_DEPTH: max_depth}

qmgr = pymqi.connect(queue_manager, channel, conn_info)

pcf = pymqi.PCFExecute(qmgr)
pcf.MQCMD_CREATE_Q(args)

qmgr.disconnect()
