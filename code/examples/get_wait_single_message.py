# See discussion and more examples at http://packages.python.org/pymqi/examples.html
# or in doc/sphinx/examples.rst in the source distribution.

import CMQC
import pymqi

queue_manager = "QM01"
channel = "SVRCONN.1"
host = "192.168.1.135"
port = "1434"
queue_name = "TEST.1"
conn_info = "%s(%s)" % (host, port)

# Message Descriptor
md = pymqi.MD()

# Get Message Options
gmo = pymqi.GMO()
gmo.Options = CMQC.MQGMO_WAIT | CMQC.MQGMO_FAIL_IF_QUIESCING
gmo.WaitInterval = 5000 # 5 seconds

qmgr = pymqi.connect(queue_manager, channel, conn_info)

queue = pymqi.Queue(qmgr, queue_name)
message = queue.get(None, md, gmo)
queue.close()

qmgr.disconnect()
