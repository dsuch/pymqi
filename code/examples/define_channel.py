# See discussion and more examples at http://packages.python.org/pymqi/examples.html
# or in doc/sphinx/examples.rst in the source distribution.

import pymqi

queue_manager = 'QM01'
channel = 'SVRCONN.1'
host = '192.168.1.135'
port = '1434'
conn_info = '%s(%s)' % (host, port)

channel_name = 'MYCHANNEL.1'
channel_type = pymqi.CMQXC.MQCHT_SVRCONN

args = {pymqi.CMQCFC.MQCACH_CHANNEL_NAME: channel_name,
        pymqi.CMQCFC.MQIACH_CHANNEL_TYPE: channel_type}

qmgr = pymqi.connect(queue_manager, channel, conn_info)

pcf = pymqi.PCFExecute(qmgr)
pcf.MQCMD_CREATE_CHANNEL(args)

qmgr.disconnect()
