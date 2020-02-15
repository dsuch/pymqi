# More examples are at https://dsuch.github.io/pymqi/examples.html
# or in code/examples in the source distribution.

import pymqi

queue_manager = 'QM1'
channel = 'DEV.APP.SVRCONN'
host = '127.0.0.1'
port = '1414'
queue_name = 'TEST.1'
message = 'Hello from Python!'
conn_info = '%s(%s)' % (host, port)
user = 'app'
password = 'password'

qmgr = pymqi.QueueManager(None)
qmgr.connect_tcp_client(queue_manager, pymqi.CD(), channel, conn_info)

try:
    qmgr.connect_tcp_client(queue_manager, pymqi.CD(), channel, conn_info)
except pymqi.MQMIError as e:
    if e.comp == pymqi.CMQC.MQCC_WARNING and e.reason == pymqi.CMQC.MQRC_ALREADY_CONNECTED:
        pass

queue = pymqi.Queue(qmgr, queue_name)
queue.put(message)
queue.close()

qmgr.disconnect()
