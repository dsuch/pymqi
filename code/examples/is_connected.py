# See discussion and more examples at http://packages.python.org/pymqi/examples.html
# or in doc/sphinx/examples.rst in the source distribution.

import logging

import pymqi
import CMQC

logging.basicConfig(level=logging.INFO)

queue_manager = "QM01"
channel = "SVRCONN.1"
host = "192.168.1.135"
port = "1434"
conn_info = "%s(%s)" % (host, port)

qmgr = pymqi.connect(queue_manager, channel, conn_info)

logging.info("qmgr.is_connected=[%s]" % qmgr.is_connected)

qmgr.disconnect()
