# More examples are at https://dsuch.github.io/pymqi/examples.html
# or in code/examples in the source distribution.

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

with pymqi.connect(queue_manager, channel, conn_info, user, password) as qmgr:
    md = pymqi.MD()
    
    with pymqi.Queue(qmgr, queue_name) as queue:
        message = queue.get(None, md)
    
        reply_to_queue_name = md.ReplyToQ.strip()
    
    with pymqi.Queue(qmgr, reply_to_queue_name) as reply_to_queue:
        reply_to_queue.put(message)    
