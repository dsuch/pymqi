# More examples are at https://dsuch.github.io/pymqi/examples.html
# or in code/examples in the source distribution.

import pymqi

queue_manager = 'QM1'
channel = 'DEV.APP.SVRCONN'
host = '127.0.0.1'
port = '1414'
conn_info = '%s(%s)' % (host, port)
user = 'app'
password = 'password'
message = 'Please reply to a dynamic queue, thanks.'
dynamic_queue_prefix = 'MY.REPLIES.*'
request_queue = 'TEST.1'

qmgr = pymqi.connect(queue_manager, channel, conn_info, user, password)

# Dynamic queue's object descriptor.
dyn_od = pymqi.OD()
dyn_od.ObjectName = 'SYSTEM.DEFAULT.MODEL.QUEUE'
dyn_od.DynamicQName = dynamic_queue_prefix

# Open the dynamic queue.
dyn_input_open_options = pymqi.CMQC.MQOO_INPUT_EXCLUSIVE
dyn_queue = pymqi.Queue(qmgr, dyn_od, dyn_input_open_options)
dyn_queue_name = dyn_od.ObjectName.strip()

# Prepare a Message Descriptor for the request message.
md = pymqi.MD()
md.ReplyToQ = dyn_queue_name

# Send the message.
queue = pymqi.Queue(qmgr, request_queue)
queue.put(message, md)

# Get and process the response here..

dyn_queue.close()
queue.close()
qmgr.disconnect()
