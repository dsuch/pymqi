# See discussion and more examples at http://packages.python.org/pymqi/examples.html
# or in doc/sphinx/examples.rst in the source distribution.

import pymqi

queue_manager = 'QM01'
channel = 'SVRCONN.1'
host = '192.168.1.135'
port = '1434'
queue_name = 'TEST.1'
message = 'Hello from Python!'
conn_info = '%s(%s)' % (host, port)

cd = pymqi.CD()

cd.ChannelName = channel
cd.ConnectionName = conn_info
cd.ChannelType = pymqi.CMQC.MQCHT_CLNTCONN
cd.TransportType = pymqi.CMQC.MQXPT_TCP

connect_options = pymqi.CMQC.MQCNO_HANDLE_SHARE_BLOCK

qmgr = pymqi.QueueManager(None)

for x in range(10):
    qmgr.connect_with_options(queue_manager, cd=cd, opts=connect_options)
    qmgr.connect_with_options(queue_manager, cd=cd, opts=connect_options)

queue = pymqi.Queue(qmgr, queue_name)
queue.put(message)
queue.close()

qmgr.disconnect()
