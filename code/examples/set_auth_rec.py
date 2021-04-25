# More examples are at https://dsuch.github.io/pymqi/examples.html
# or in code/examples in the source distribution.

import logging

import pymqi

logging.basicConfig(level=logging.INFO)

queue_manager = 'QM1'
channel = 'CHANNEL.1'
host = '127.0.0.1'
port = '1414'
conn_info = '%s(%s)' % (host, port)
user = 'app'
password = 'password'

qmgr = pymqi.connect(queue_manager, channel, conn_info, user, password)
pcf = pymqi.PCFExecute(qmgr)

group_entity = [b'swww02']
auth_entity = [pymqi.CMQCFC.MQAUTH_BROWSE]

args = {pymqi.CMQCFC.MQCACF_AUTH_PROFILE_NAME: 'Q1',
        pymqi.CMQCFC.MQIACF_OBJECT_TYPE: pymqi.CMQC.MQOT_Q,
        pymqi.CMQCFC.MQIACF_AUTH_ADD_AUTHS: auth_entity,
        pymqi.CMQCFC.MQCACF_GROUP_ENTITY_NAMES: group_entity}


result = pcf.MQCMD_SET_AUTH_REC(args)

qmgr.disconnect()
