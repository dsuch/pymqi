# See discussion and more examples at http://packages.python.org/pymqi/examples.html
# or in doc/sphinx/examples.rst in the source distribution.

import pymqi

queue_manager = 'QM1'
channel = 'DEV.APP.SVRCONN'
host = '127.0.0.1'
port = '1414'
queue_name = 'TEST.1'
message = 'Hello from Python!'
alternate_user_id = 'myuser'
conn_info = '%s(%s)' % (host, port)
user = 'app'
password = 'password'

qmgr = pymqi.connect(queue_manager, channel, conn_info, user, password)

od = pymqi.OD()
od.ObjectName = queue_name
od.AlternateUserId = alternate_user_id

queue = pymqi.Queue(qmgr)
queue.open(od, pymqi.CMQC.MQOO_OUTPUT | pymqi.CMQC.MQOO_ALTERNATE_USER_AUTHORITY)
queue.put(message)

queue.close()
qmgr.disconnect()
