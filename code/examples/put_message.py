# More examples are at https://dsuch.github.io/pymqi/examples.html
# or in code/examples in the source distribution.

import pymqi

queue_manager = "QM01"
channel = 'DEV.APP.SVRCONN'
host = '127.0.0.1'
port = '1414'
queue_name = 'TEST.1'
message = 'Hello from Python!'
conn_info = '%s(%s)' % (host, port)
user = 'app'
password = 'password'

with pymqi.connect(queue_manager, channel, conn_info, user, password) as qmgr:
    with pymqi.Queue(qmgr, queue_name) as queue:
        queue.put(message)
