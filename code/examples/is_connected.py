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

qmgr = pymqi.connect(queue_manager, channel, conn_info, user, password)

logging.info('qmgr.is_connected=`%s`' % qmgr.is_connected)

qmgr.disconnect()
