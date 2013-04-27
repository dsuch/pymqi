# See discussion and more examples at http://packages.python.org/pymqi/examples.html
# or in doc/sphinx/examples.rst in the source distribution.

import logging

import pymqi
import CMQC, CMQCFC, CMQXC

logging.basicConfig(level=logging.INFO)

queue_manager = 'QM01'
channel = 'CHANNEL.1'
host = '127.0.0.1'
port = '1434'
conn_info = '%s(%s)' % (host, port)

qmgr = pymqi.connect(queue_manager, channel, conn_info)
pcf = pymqi.PCFExecute(qmgr)

groupEntity ={128L: ['swww02']}
authEntity = {128L: [CMQCFC.MQAUTH_BROWSE]}

args = {CMQCFC.MQCACF_AUTH_PROFILE_NAME: 'Q1',
        CMQCFC.MQIACF_OBJECT_TYPE: CMQC.MQOT_Q,
        CMQCFC.MQIACF_AUTH_ADD_AUTHS: authEntity,
        CMQCFC.MQCACF_GROUP_ENTITY_NAMES: groupEntity}


result = pcf.MQCMD_SET_AUTH_REC(args)

qmgr.disconnect()

