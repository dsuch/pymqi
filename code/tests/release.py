# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function

# Run this module on each supported MQ version prior to releasing PyMQI.

# stdlib
from uuid import uuid4

# PyMQI
import pymqi
from pymqi import CMQC
from pymqi import CMQCFC

queue_manager = 'MQTEST'
channel = 'CH1'
host = '127.0.0.1'
port = '8887'
conn_info = '{0}({1})'.format(host, port)

queue_name = uuid4().hex.encode('ascii')
message = uuid4().hex.encode('ascii')

# Connect ..
qmgr = pymqi.connect(queue_manager, channel, conn_info)
pcf = pymqi.PCFExecute(qmgr)

# .. create a queue ..
pcf.MQCMD_CREATE_Q({CMQC.MQCA_Q_NAME: queue_name, CMQC.MQIA_Q_TYPE: CMQC.MQQT_LOCAL})

# .. put a message ..
queue = pymqi.Queue(qmgr, queue_name)
queue.put(message)
queue.close()

# .. get it back ..
queue = pymqi.Queue(qmgr, queue_name)
assert queue.get() == message
queue.close()

# .. drop the queue ..
pcf.MQCMD_DELETE_Q({CMQC.MQCA_Q_NAME: queue_name, CMQC.MQIA_Q_TYPE: CMQC.MQQT_LOCAL})

# .. and just to be sure, grab some channels as well ..
result = pcf.MQCMD_INQUIRE_CHANNEL({CMQCFC.MQCACH_CHANNEL_NAME: b'*'})
assert len(result) > 1

# .. finally, close the connection.
qmgr.disconnect()
