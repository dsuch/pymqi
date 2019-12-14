# See discussion and more examples at http://packages.python.org/pymqi/examples.html
# or in doc/sphinx/examples.rst in the source distribution.

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
queue_type = pymqi.CMQC.MQQT_MODEL

args = {pymqi.CMQC.MQCA_Q_NAME: prefix, pymqi.CMQC.MQIA_Q_TYPE: queue_type}

qmgr = pymqi.connect(queue_manager, channel, conn_info, user, password)
pcf = pymqi.PCFExecute(qmgr)

try:
    response = pcf.MQCMD_INQUIRE_Q(args)
except pymqi.MQMIError as e:
    if e.comp == pymqi.CMQC.MQCC_FAILED and e.reason == pymqi.CMQC.MQRC_UNKNOWN_OBJECT_NAME:
        logging.info('No queues matched given arguments.')
    else:
        raise
else:
    for queue_info in response:
        queue_name = queue_info[pymqi.CMQC.MQCA_Q_NAME]
        logging.info('Found queue `%s`' % queue_name)

qmgr.disconnect()
