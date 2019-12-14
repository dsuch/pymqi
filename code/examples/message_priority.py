# See discussion and more examples at http://packages.python.org/pymqi/examples.html
# or in doc/sphinx/examples.rst in the source distribution.

import logging

import pymqi

logging.basicConfig(level=logging.INFO)

queue_manager = 'QM01'
channel = 'SVRCONN.1'
host = '192.168.1.135'
port = '1434'
queue_name = 'TEST.1'
message = 'Hello from Python!'
conn_info = '%s(%s)' % (host, port)
priority = 2

put_md = pymqi.MD()
put_md.Priority = priority

qmgr = pymqi.connect(queue_manager, channel, conn_info)

put_queue = pymqi.Queue(qmgr, queue_name)
put_queue.put(message, put_md)

get_md = pymqi.MD()
get_queue = pymqi.Queue(qmgr, queue_name)
message_body = get_queue.get(None, get_md)

logging.info('Received a message, priority `%s`.' % get_md.Priority)

put_queue.close()
get_queue.close()
qmgr.disconnect()
