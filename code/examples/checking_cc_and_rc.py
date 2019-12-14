# See discussion and more examples at http://packages.python.org/pymqi/examples.html
# or in doc/sphinx/examples.rst in the source distribution.

import logging

import pymqi

queue_manager = 'QM1'
channel = 'DEV.APP.SVRCONN'
host = 'localhost.invalid' # Note the invalid hostname here
port = '1414'
conn_info = '%s(%s)' % (host, port)
user = 'app'
password = 'password'

try:
    qmgr = pymqi.connect(queue_manager, channel, conn_info, user, password)
except pymqi.MQMIError as e:
    if e.comp == pymqi.CMQC.MQCC_FAILED and e.reason == pymqi.CMQC.MQRC_HOST_NOT_AVAILABLE:
        logging.error('Such a host `%s` does not exist.' % host)
