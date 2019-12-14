# See discussion and more examples at http://packages.python.org/pymqi/examples.html
# or in doc/sphinx/examples.rst in the source distribution.

import pymqi

queue_manager = 'QM1'
channel = 'DEV.APP.SVRCONN'
host = '127.0.0.1'
port = '1414'
queue_name = 'TEST.1'
message = 'Here is the reply'
conn_info = '%s(%s)' % (host, port)
user = 'app'
password = 'password'

qmgr = pymqi.connect(queue_manager, channel, conn_info, user, password)

md = pymqi.MD()

queue = pymqi.Queue(qmgr, queue_name)
message = queue.get(None, md)

reply_to_queue_name = md.ReplyToQ.strip()
reply_to_queue = pymqi.Queue(qmgr, reply_to_queue_name)
reply_to_queue.put(message)

queue.close()
qmgr.disconnect()
