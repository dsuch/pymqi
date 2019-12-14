# See discussion and more examples at http://packages.python.org/pymqi/examples.html
# or in doc/sphinx/examples.rst in the source distribution.

import pymqi

queue_manager = "QM01"
channel = "SVRCONN.1"
host = "192.168.1.135"
port = "1434"
queue_name = "TEST.1"
message = "Hello from Python!"
conn_info = "%s(%s)" % (host, port)

qmgr = pymqi.QueueManager(None)
qmgr.connect_tcp_client(queue_manager, pymqi.CD(), channel, conn_info)

try:
    qmgr.connect_tcp_client(queue_manager, pymqi.CD(), channel, conn_info)
except pymqi.MQMIError as e:
    if e.comp == pymqi.CMQC.MQCC_WARNING and e.reason == pymqi.CMQC.MQRC_ALREADY_CONNECTED:
        # Move along, nothing to see here..
        pass

queue = pymqi.Queue(qmgr, queue_name)
queue.put(message)
queue.close()

qmgr.disconnect()
