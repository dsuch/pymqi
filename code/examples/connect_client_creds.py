# See discussion and more examples at http://packages.python.org/pymqi/examples.html
# or in doc/sphinx/examples.rst in the source distribution.

import pymqi

queue_manager = 'QM01'
channel = 'SVRCONN.1'
host = '192.168.1.135'
port = '1434'
conn_info = '%s(%s)' % (host, port)

user = 'myuser'
password = 'mypassword'

qmgr = pymqi.connect(queue_manager, channel, conn_info, user, password)
qmgr.disconnect()
