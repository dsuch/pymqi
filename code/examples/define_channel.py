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

channel_name = 'MYCHANNEL.1'
channel_type = pymqi.CMQXC.MQCHT_SVRCONN

args = {
    pymqi.CMQCFC.MQCACH_CHANNEL_NAME: channel_name,
    pymqi.CMQCFC.MQIACH_CHANNEL_TYPE: channel_type
}

with pymqi.connect(queue_manager, channel, conn_info, user, password) as qmgr:
    pcf = pymqi.PCFExecute(qmgr)
    pcf.MQCMD_CREATE_CHANNEL(args)
