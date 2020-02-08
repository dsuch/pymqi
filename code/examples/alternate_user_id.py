# More examples are at https://dsuch.github.io/pymqi/examples.html
# or in code/examples in the source distribution.

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

od = pymqi.OD()
od.ObjectName = queue_name
od.AlternateUserId = alternate_user_id

with pymqi.connect(queue_manager, channel, conn_info, user, password) as qmgr:
    with pymqi.Queue(qmgr) as queue:
        queue.open(od, pymqi.CMQC.MQOO_OUTPUT | pymqi.CMQC.MQOO_ALTERNATE_USER_AUTHORITY)
        queue.put(message)
