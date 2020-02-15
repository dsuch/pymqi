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

queue_name = 'MYQUEUE.1'
queue_type = pymqi.CMQC.MQQT_LOCAL
max_depth = 123456

args = {
    pymqi.CMQC.MQCA_Q_NAME: queue_name,
    pymqi.CMQC.MQIA_Q_TYPE: queue_type,
    pymqi.CMQC.MQIA_MAX_Q_DEPTH: max_depth
}

qmgr = pymqi.connect(queue_manager, channel, conn_info, user, password)

pcf = pymqi.PCFExecute(qmgr)
pcf.MQCMD_CREATE_Q(args)

qmgr.disconnect()
