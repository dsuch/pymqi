# More examples are at https://dsuch.github.io/pymqi/examples.html
# or in code/examples in the source distribution.

import logging

import pymqi

logging.basicConfig(level=logging.INFO)

queue_manager = 'QM1'
channel = 'DEV.APP.SVRCONN'
host = '127.0.0.1'
port = '1414'
conn_info = '%s(%s)' % (host, port)
user = 'app'
password = 'password'

prefix = 'SYSTEM.*'

args = {pymqi.CMQCFC.MQCACH_CHANNEL_NAME: prefix}

qmgr = pymqi.connect(queue_manager, channel, conn_info, user, password)
pcf = pymqi.PCFExecute(qmgr)

try:
    response = pcf.MQCMD_INQUIRE_CHANNEL(args)
except pymqi.MQMIError as e:
    if e.comp == pymqi.CMQC.MQCC_FAILED and e.reason == pymqi.CMQC.MQRC_UNKNOWN_OBJECT_NAME:
        logging.info('No channels matched prefix `%s`' % prefix)
    else:
        raise
else:
    for channel_info in response:
        channel_name = channel_info[pymqi.CMQCFC.MQCACH_CHANNEL_NAME]
        logging.info('Found channel `%s`' % channel_name)

qmgr.disconnect()
