# More examples are at https://dsuch.github.io/pymqi/examples.html
# or in code/examples in the source distribution.

import logging

import pymqi

logging.basicConfig(level=logging.INFO)

queue_manager = 'QM1'
channel = 'SSL.SVRCONN.1'
host = '127.0.0.1'
port = '1414'
queue_name = 'TEST.1'
conn_info = '%s(%s)' % (host, port)
ssl_cipher_spec = 'TLS_RSA_WITH_AES_256_CBC_SHA'
key_repo_location = '/var/mqm/ssl-db/client/KeyringClient'
message = 'Hello from Python!'

cd = pymqi.CD()
cd.ChannelName = channel
cd.ConnectionName = conn_info
cd.ChannelType = pymqi.CMQC.MQCHT_CLNTCONN
cd.TransportType = pymqi.CMQC.MQXPT_TCP
cd.SSLCipherSpec = ssl_cipher_spec

sco = pymqi.SCO()
sco.KeyRepository = key_repo_location

qmgr = pymqi.QueueManager(None)
with qmgr.connect_with_options(queue_manager, cd, sco):
    with pymqi.Queue(qmgr, queue_name) as put_queue:
        put_queue.put(message)
    
    with pymqi.Queue(qmgr, queue_name) as get_queue:
        logging.info('Here is the message again: [%s]' % get_queue.get())
