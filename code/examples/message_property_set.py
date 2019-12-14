# See discussion and more examples at http://packages.python.org/pymqi/examples.html
# or in doc/sphinx/examples.rst in the source distribution.

import logging

import pymqi

logging.basicConfig(level=logging.INFO)

queue_manager = 'QM1'
channel = 'DEV.APP.SVRCONN'
host = '127.0.0.1'
port = '1414'
queue_name = 'TEST.1'
message = 'Hello from Python!'
property_name = 'Propertie_1'
conn_info = '%s(%s)' % (host, port)

qmgr = pymqi.connect(queue_manager, channel, conn_info)

put_msg_h = pymqi.MessageHandle(qmgr)
put_msg_h.properties.set(property_name, message) # Default type is CMQC.MQTYPE_STRING

pmo = pymqi.PMO(Version=pymqi.CMQC.MQPMO_VERSION_3) # PMO v3 is required propeties
pmo.OriginalMsgHandle = put_msg_h.msg_handle

put_md = pymqi.MD(Version=pymqi.CMQC.MQMD_CURRENT_VERSION)

put_queue = pymqi.Queue(qmgr, queue_name)
put_queue.put(b'', put_md, pmo)

get_msg_h = pymqi.MessageHandle(qmgr)

gmo = pymqi.GMO(Version=pymqi.CMQC.MQGMO_CURRENT_VERSION)
gmo.Options = pymqi.CMQC.MQGMO_PROPERTIES_IN_HANDLE
gmo.MsgHandle = get_msg_h.msg_handle

get_md = pymqi.MD()
get_queue = pymqi.Queue(qmgr, queue_name)
message_body = get_queue.get(None, get_md, gmo)

property_value = get_msg_h.properties.get(property_name)
logging.info('Message received. Property name: `%s`, property value: `%s`' % (property_name, property_value))

put_queue.close()
get_queue.close()
qmgr.disconnect()
