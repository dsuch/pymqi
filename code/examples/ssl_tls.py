# See discussion and more examples at http://packages.python.org/pymqi/examples.html
# or in doc/sphinx/examples.rst in the source distribution.

import logging

import pymqi

logging.basicConfig(level=logging.INFO)

queue_manager = "QM01"
channel = "SSL.SVRCONN.1"
host = "192.168.1.135"
port = "1434"
queue_name = "TEST.1"
conn_info = "%s(%s)" % (host, port)
ssl_cipher_spec = "TLS_RSA_WITH_AES_256_CBC_SHA"
key_repo_location = "/var/mqm/ssl-db/client/KeyringClient"
message = "Hello from Python!"

cd = pymqi.CD()
cd.ChannelName = channel
cd.ConnectionName = conn_info
cd.ChannelType = pymqi.CMQC.MQCHT_CLNTCONN
cd.TransportType = pymqi.CMQC.MQXPT_TCP
cd.SSLCipherSpec = ssl_cipher_spec

sco = pymqi.SCO()
sco.KeyRepository = key_repo_location

qmgr = pymqi.QueueManager(None)
qmgr.connect_with_options(queue_manager, cd, sco)

put_queue = pymqi.Queue(qmgr, queue_name)
put_queue.put(message)

get_queue = pymqi.Queue(qmgr, queue_name)
logging.info("Here's the message again: [%s]" % get_queue.get())

put_queue.close()
get_queue.close()
qmgr.disconnect()
