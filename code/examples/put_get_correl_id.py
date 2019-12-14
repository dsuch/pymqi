# See discussion and more examples at http://packages.python.org/pymqi/examples.html
# or in doc/sphinx/examples.rst in the source distribution.

# stdlib
import logging, threading, time, traceback, uuid

# PyMQI
import pymqi

logging.basicConfig(level=logging.INFO)

# Queue manager name
qm_name = "QM01"

# Listener host and port
listener = "192.168.1.135(1434)"

# Channel to transfer data through
channel = "SVRCONN.1"

# Request Queue
request_queue_name = "REQUEST.QUEUE.1"

# ReplyTo Queue
replyto_queue_name = "REPLYTO.QUEUE.1"

message_prefix = "Test Data. "

class Producer(threading.Thread):
    """ A base class for any producer used in this example.
    """
    def __init__(self):
        threading.Thread.__init__(self)
        self.daemon = True

        cd = pymqi.CD()
        cd.ChannelName = channel
        cd.ConnectionName = listener
        cd.ChannelType = pymqi.CMQC.MQCHT_CLNTCONN
        cd.TransportType = pymqi.CMQC.MQXPT_TCP
        self.qm = pymqi.QueueManager(None)
        self.qm.connect_with_options(qm_name, opts=pymqi.CMQC.MQCNO_HANDLE_SHARE_NO_BLOCK,
                                   cd=cd)

        self.req_queue = pymqi.Queue(self.qm, request_queue_name)
        self.replyto_queue = pymqi.Queue(self.qm, replyto_queue_name)


class RequestProducer(Producer):
    """ Instances of this class produce an infinite stream of request messages
    and wait for appropriate responses on reply-to queues.
    """

    def run(self):

        while True:
            # Put the request message.
            put_mqmd = pymqi.MD()

            # Set the MsgType to request.
            put_mqmd["MsgType"] = pymqi.CMQC.MQMT_REQUEST

            # Set up the ReplyTo QUeue/Queue Manager (Queue Manager is automatically
            # set by MQ).

            put_mqmd["ReplyToQ"] = replyto_queue_name
            put_mqmd["ReplyToQMgr"] = qm_name

            # Set up the put options - must do with NO_SYNCPOINT so that the request
            # message is committed immediately.
            put_opts = pymqi.PMO(Options=pymqi.CMQC.MQPMO_NO_SYNCPOINT + pymqi.CMQC.MQPMO_FAIL_IF_QUIESCING)

            # Create a random message.
            message = message_prefix + uuid.uuid4().hex

            self.req_queue.put(message, put_mqmd, put_opts)
            logging.info("Put request message.  Message: [%s]" % message)

            # Set up message descriptor for get.
            get_mqmd = pymqi.MD()

            # Set the get CorrelId to the put MsgId (which was set by MQ on the put1).
            get_mqmd["CorrelId"] = put_mqmd["MsgId"]

            # Set up the get options.
            get_opts = pymqi.GMO(Options=pymqi.CMQC.MQGMO_NO_SYNCPOINT +
                                         pymqi.CMQC.MQGMO_FAIL_IF_QUIESCING +
                                         pymqi.CMQC.MQGMO_WAIT)

            # Version must be set to 2 to correlate.
            get_opts["Version"] = pymqi.CMQC.MQGMO_VERSION_2

            # Tell MQ that we are matching on CorrelId.
            get_opts["MatchOptions"] = pymqi.CMQC.MQMO_MATCH_CORREL_ID

            # Set the wait timeout of half a second.
            get_opts["WaitInterval"] = 500

            # Open the replyto queue and get response message,
            replyto_queue = pymqi.Queue(self.qm, replyto_queue_name, pymqi.CMQC.MQOO_INPUT_SHARED)
            response_message = replyto_queue.get(None, get_mqmd, get_opts)

            logging.info("Got response message [%s]" % response_message)

            time.sleep(1)

class ResponseProducer(Producer):
    """ Instances of this class wait for request messages and produce responses.
    """

    def run(self):

        # Request message descriptor, will be reset after processing each
        # request message.
        request_md = pymqi.MD()

        # Get Message Options
        gmo = pymqi.GMO()
        gmo.Options = pymqi.CMQC.MQGMO_WAIT | pymqi.CMQC.MQGMO_FAIL_IF_QUIESCING
        gmo.WaitInterval = 500 # Half a second

        queue = pymqi.Queue(self.qm, request_queue_name)

        keep_running = True

        while keep_running:
            try:
                # Wait up to to gmo.WaitInterval for a new message.
                request_message = queue.get(None, request_md, gmo)

                # Create a response message descriptor with the CorrelId
                # set to the value of MsgId of the original request message.
                response_md = pymqi.MD()
                response_md.CorrelId = request_md.MsgId

                response_message = "Response to message %s" % request_message
                self.replyto_queue.put(response_message, response_md)

                # Reset the MsgId, CorrelId & GroupId so that we can reuse
                # the same 'md' object again.
                request_md.MsgId = pymqi.CMQC.MQMI_NONE
                request_md.CorrelId = pymqi.CMQC.MQCI_NONE
                request_md.GroupId = pymqi.CMQC.MQGI_NONE

            except pymqi.MQMIError as e:
                if e.comp == pymqi.CMQC.MQCC_FAILED and e.reason == pymqi.CMQC.MQRC_NO_MSG_AVAILABLE:
                    # No messages, that's OK, we can ignore it.
                    pass
                else:
                    # Some other error condition.
                    raise

req = RequestProducer()
resp = ResponseProducer()

req.start()
resp.start()

try:
    while True:
        time.sleep(0.1)
except KeyboardInterrupt:
    req.qm.disconnect()
