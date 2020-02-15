# More examples are at https://dsuch.github.io/pymqi/examples.html
# or in code/examples in the source distribution.

import pymqi

queue_manager = 'QM1'
channel = 'DEV.APP.SVRCONN'
host = '127.0.0.1'
port = '1414'
queue_name = 'TEST.1'
conn_info = '%s(%s)' % (host, port)
user = 'app'
password = 'password'

qmgr = pymqi.connect(queue_manager, channel, conn_info, user, password)

queue = pymqi.Queue(qmgr, queue_name)
message = queue.get()
queue.close()

qmgr.disconnect()
