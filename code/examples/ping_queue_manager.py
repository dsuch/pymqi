# See discussion and more examples at http://packages.python.org/pymqi/examples.html
# or in doc/sphinx/examples.rst in the source distribution.

import pymqi
import CMQC, CMQCFC, CMQXC

queue_manager = "QM01"
channel = "SVRCONN.1"
host = "192.168.1.135"
port = "1434"
conn_info = "%s(%s)" % (host, port)

qmgr = pymqi.connect(queue_manager, channel, conn_info)

pcf = pymqi.PCFExecute(qmgr)
pcf.MQCMD_PING_Q_MGR()

qmgr.disconnect()
