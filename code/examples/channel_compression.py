# See discussion and more examples at http://packages.python.org/pymqi/examples.html
# or in doc/sphinx/examples.rst in the source distribution.

import pymqi

queue_manager = 'QM01'
channel = 'SVRCONN.1'
host = '192.168.1.135'
port = '1434'
queue_name = 'TEST.1'
message = 'Hello from Python!' * 10000
conn_info = '%s(%s)' % (host, port)

cd = pymqi.CD()
cd.MsgCompList[1] = pymqi.CMQXC.MQCOMPRESS_ZLIBHIGH

qmgr = pymqi.connect(queue_manager, channel, conn_info)

queue = pymqi.Queue(qmgr, queue_name)
queue.put(message)
queue.close()

qmgr.disconnect()
