# More examples are at https://dsuch.github.io/pymqi/examples.html
# or in code/examples in the source distribution.

import pymqi

queue_manager = 'QM1'
channel = 'DEV.APP.SVRCONN'
host = '127.0.0.1'
port = '1414'
queue_name = 'TEST.1'
conn_info = '%s(%s)' % (host, port)
user = 'app'
password = 'password'

# Message Descriptor
md = pymqi.MD()

# Get Message Options
gmo = pymqi.GMO()
gmo.Options = pymqi.CMQC.MQGMO_WAIT | pymqi.CMQC.MQGMO_FAIL_IF_QUIESCING
gmo.WaitInterval = 5000 # 5 seconds

with pymqi.connect(queue_manager, channel, conn_info, user, password) as qmgr:
    with pymqi.Queue(qmgr, queue_name) as queue:
        message = queue.get(None, md, gmo)
