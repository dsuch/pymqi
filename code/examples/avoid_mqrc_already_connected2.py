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
