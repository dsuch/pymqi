# More examples are at https://dsuch.github.io/pymqi/examples.html
# or in code/examples in the source distribution.

import logging

import pymqi

logging.basicConfig(level=logging.INFO)

queue_manager = 'QM1'
channel = 'DEV.APP.SVRCONN'
host = '127.0.0.1'
port = '1414'
queue_name = 'TEST.1'
message = 'Hello from Python!'
priority = 2
conn_info = '%s(%s)' % (host, port)
user = 'app'
password = 'password'

put_md = pymqi.MD()
put_md.Priority = priority

with pymqi.connect(queue_manager, channel, conn_info, user, password) as qmgr:
    with pymqi.Queue(qmgr, queue_name) as put_queue:
        put_queue.put(message, put_md)
    
    get_md = pymqi.MD()
    with pymqi.Queue(qmgr, queue_name) as get_queue:
        message_body = get_queue.get(None, get_md)
    
        logging.info('Received a message, priority `%s`.' % get_md.Priority)
    
