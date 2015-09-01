# See discussion and more examples at http://packages.python.org/pymqi/examples.html
# or in doc/sphinx/examples.rst in the source distribution.

import logging

import pymqi

queue_manager = "QM01"
channel = "SVRCONN.1"
host = "foo.bar" # Note the made up host name
port = "1434"
conn_info = "%s(%s)" % (host, port)

try:
    qmgr = pymqi.connect(queue_manager, channel, conn_info)
except pymqi.MQMIError, e:
    if e.comp == pymqi.CMQC.MQCC_FAILED and e.reason == pymqi.CMQC.MQRC_HOST_NOT_AVAILABLE:
        logging.error("Such a host [%s] does not exist." % host)
