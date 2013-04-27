# See discussion and more examples at http://packages.python.org/pymqi/examples.html
# or in doc/sphinx/examples.rst in the source distribution.

import CMQC
import pymqi

queue_manager = "QM01"
channel = "SVRCONN.1"
host = "192.168.1.135"
port = "1434"
queue_name = "TEST.1"
conn_info = "%s(%s)" % (host, port)

# Message Descriptor
md = pymqi.MD()

# Get Message Options
gmo = pymqi.GMO()
gmo.Options = CMQC.MQGMO_WAIT | CMQC.MQGMO_FAIL_IF_QUIESCING
gmo.WaitInterval = 5000 # 5 seconds

qmgr = pymqi.connect(queue_manager, channel, conn_info)
queue = pymqi.Queue(qmgr, queue_name)

keep_running = True

while keep_running:
    try:
        # Wait up to to gmo.WaitInterval for a new message.
        message = queue.get(None, md, gmo)

        # Process the message here..

        # Reset the MsgId, CorrelId & GroupId so that we can reuse
        # the same 'md' object again.
        md.MsgId = CMQC.MQMI_NONE
        md.CorrelId = CMQC.MQCI_NONE
        md.GroupId = CMQC.MQGI_NONE

    except pymqi.MQMIError, e:
        if e.comp == CMQC.MQCC_FAILED and e.reason == CMQC.MQRC_NO_MSG_AVAILABLE:
            # No messages, that's OK, we can ignore it.
            pass
        else:
            # Some other error condition.
            raise

queue.close()
qmgr.disconnect()
