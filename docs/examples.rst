Examples
========

.. note::

    Sponsored by `Zato <https://zato.io/docs?pymqi-e01>`_ - Open-Source ESB, SOA, REST, APIs and Cloud Integrations in Python

The purpose of this section is to gather code showing PyMQI in action or code
that's related to common IBM MQ-related tasks in general. Some of the
examples are Python ports of IBM's examples that IBM MQ ships with.

The samples are self-contained and ready to use in your own PyMQI applications.
Don't hesitate to :doc:`send a question <./support>`
if you'd like to see any specific example be added. Thanks!

===============================
Connecting in client mode
===============================

Code::

    import pymqi

    queue_manager = 'QM1'
    channel = 'DEV.APP.SVRCONN'
    host = '127.0.0.1'
    port = '1414'
    conn_info = '%s(%s)' % (host, port)

    qmgr = pymqi.connect(queue_manager, channel, conn_info)
    qmgr.disconnect()

============================================================
Connecting in client mode with username/password credentials
============================================================

Code::

    import pymqi

    queue_manager = 'QM1'
    channel = 'DEV.APP.SVRCONN'
    host = '127.0.0.1'
    port = '1414'
    conn_info = '%s(%s)' % (host, port)

    user = 'app'
    password = 'mypassword'

    qmgr = pymqi.connect(queue_manager, channel, conn_info, user, password)
    qmgr.disconnect()

Notes:

* Connecting with username/password credentials was added in PyMQI 1.5
* The functionality requires IBM MQ 8.0+ queue managers
* Credentials need to be provided to PyMQI as regular Python variables - PyMQI will not look them
  up in any user database or similar

===============================
Connecting in bindings mode
===============================

Code::

    import pymqi

    queue_manager = 'QM1'
    qmgr = pymqi.connect(queue_manager)

    qmgr.disconnect()

====================================
How to put the message on a queue
====================================

Code::

    import pymqi

    queue_manager = 'QM1'
    channel = 'DEV.APP.SVRCONN'
    host = '127.0.0.1'
    port = '1414'
    queue_name = 'TEST.1'
    message = 'Hello from Python!'
    conn_info = '%s(%s)' % (host, port)

    qmgr = pymqi.connect(queue_manager, channel, conn_info)

    queue = pymqi.Queue(qmgr, queue_name)
    queue.put(message)
    queue.close()

    qmgr.disconnect()

====================================
How to get the message off a queue
====================================

Code::

    import pymqi

    queue_manager = 'QM1'
    channel = 'DEV.APP.SVRCONN'
    host = '127.0.0.1'
    port = '1414'
    queue_name = 'TEST.1'
    conn_info = '%s(%s)' % (host, port)

    qmgr = pymqi.connect(queue_manager, channel, conn_info)

    queue = pymqi.Queue(qmgr, queue_name)
    message = queue.get()
    queue.close()

    qmgr.disconnect()

Notes:

* By default Queue.get will not use any timeout, if messages are not available
  immediately a pymqi.MQMIError will be raised with MQ reason code set to
  2033 MQRC_NO_MSG_AVAILABLE, see :ref:`here <wait_single_message>`
  and :ref:`here <wait_multiple_messages>` for info on how to wait for a single or multiple messages.

==============================
Sending Unicode data vs. bytes
==============================

* Note that Unicode and bytes handling is unified in PyMQI regardless of whether one uses Python 2 or 3, i.e.
  everything below applies to both Python lines

* PyMQI does not process in any way bytes objects used in **queue.put** calls - this means that if you encode
  your data as bytes before handling it to queue.put, the data will be sent as-is

* If you give queue.put Unicode objects on input, though, they will be automatically converted to bytes,
  using **UTF-8** by default - this should suffice in most cases

* It is possible to change the default encoding used for conversion from Unicode to bytes by providing
  two parameters when calling **pymqi.connect** or when constructing **QueueManager** objects

* The parameters are called **bytes_encoding** and **default_ccsid** and their default values are **utf8** and **1208**,
  respectively

* Parameter bytes_encoding is used for conversion of Python Unicode objects to bytes objects

* Parameter default_ccsid is used to specify a CCSID in the underlying call's MQMD structure

* Both parameters will be used in all put calls related to a single MQ connection - that is, they are specified once only
  on the level of the connection to a queue manager, rather than individually for each put call

* If not using the defaults, it is the user's responsibility to make sure that the two parameters match - for instance,
  encoding UTF-8 is represented by CCSID 1208, but a different CCSID may be required with other encodings

* It is also the user's responsibility to ensure that default_ccsid matches the queue manager's CCSID

* Again, the conversion from Unicode to bytes as well as the application of bytes_encoding and default_ccsid take place
  only if Unicode objects are given on input to queue.put - if data is already bytes, there is no conversion

* In the example below, message is a Unicode object and it will be converted to ISO-8859-1 by PyMQI
  because this is the encoding explicitly specified. Also, that encoding's corresponding CCSID - 819 - is given on input
  to pymqi.connect.

Code::

    import pymqi

    queue_manager = 'QM1'
    channel = 'DEV.APP.SVRCONN'
    host = '127.0.0.1'
    port = '1414'
    queue_name = 'TEST.1'
    message = u'My Unicode data'
    conn_info = '%s(%s)' % (host, port)

    bytes_encoding = 'iso-8859-1'
    default_ccsid = 819

    qmgr = pymqi.connect(queue_manager, channel, conn_info, bytes_encoding=bytes_encoding, default_ccsid=default_ccsid)

    queue = pymqi.Queue(qmgr, queue_name)
    queue.put(message)
    queue.close()

    qmgr.disconnect()

=================================================
How to get a message without JMS (MQRFH2) headers
=================================================

Code::

    import pymqi

    queue_manager = 'QM1'
    channel = 'DEV.APP.SVRCONN'
    host = '127.0.0.1'
    port = '1414'
    queue_name = 'TEST.1'
    conn_info = '%s(%s)' % (host, port)

    qmgr = pymqi.connect(queue_manager, channel, conn_info)

    queue = pymqi.Queue(qmgr, queue_name)

    # Get the message but discard any JMS headers
    message = queue.get_no_jms()

    # Works exactly as above: get_no_rfh2 is an alias to get_no_jms
    message = queue.get_no_rfh2()

    # Close queue and disconnect from queue manager
    queue.close()
    qmgr.disconnect()

Notes:

* Depending on how they are configured, JMS-based applications may send a series of headers
  that are at times not required by Python recipients - use .get_no_jms to receive only
  business payload without any JMS headers.

* For completeness, .get_no_rfh2 was added as an alias to .get_no_jms - it works exactly the same.

.. _wait_single_message:

====================================
How to wait for a single message
====================================

Code::

    import pymqi

    queue_manager = 'QM1'
    channel = 'DEV.APP.SVRCONN'
    host = '127.0.0.1'
    port = '1414'
    queue_name = 'TEST.1'
    conn_info = '%s(%s)' % (host, port)

    # Message Descriptor
    md = pymqi.MD()

    # Get Message Options
    gmo = pymqi.GMO()
    gmo.Options = pymqi.CMQC.MQGMO_WAIT | pymqi.CMQC.MQGMO_FAIL_IF_QUIESCING
    gmo.WaitInterval = 5000 # 5 seconds

    qmgr = pymqi.connect(queue_manager, channel, conn_info)

    queue = pymqi.Queue(qmgr, queue_name)
    message = queue.get(None, md, gmo)
    queue.close()

    qmgr.disconnect()

Notes:

* If not told otherwise, Queue.get builds up a default Message Descriptor (MD) and
  Get Message Options (GMO), however in this case one needs to specify custom
  GMO in order to tell MQ to wait for messages for a given time. A default MD
  still needs to be passed to Queue.get,

* It is a recommended MQ programming practice to always use MQGMO_FAIL_IF_QUIESCING -
  PyMQI uses it by default unless it's overridden.

.. _wait_multiple_messages:

====================================
How to wait for multiple messages
====================================

Code::

    import pymqi

    queue_manager = 'QM1'
    channel = 'DEV.APP.SVRCONN'
    host = '127.0.0.1'
    port = '1414'
    queue_name = 'TEST.1'
    conn_info = '%s(%s)' % (host, port)

    # Message Descriptor
    md = pymqi.MD()

    # Get Message Options
    gmo = pymqi.GMO()
    gmo.Options = pymqi.CMQC.MQGMO_WAIT | pymqi.CMQC.MQGMO_FAIL_IF_QUIESCING
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
            md.MsgId = pymqi.CMQC.MQMI_NONE
            md.CorrelId = pymqi.CMQC.MQCI_NONE
            md.GroupId = pymqi.CMQC.MQGI_NONE

        except pymqi.MQMIError as e:
            if e.comp == pymqi.CMQC.MQCC_FAILED and e.reason == pymqi.CMQC.MQRC_NO_MSG_AVAILABLE:
                # No messages, that is OK, we can ignore it.
                pass
            else:
                # Some other error condition.
                raise

    queue.close()
    qmgr.disconnect()

Notes:

* The key part is a GIL-releasing non-busy loop which consumes almost no CPU and runs very
  close to raw C speed. On modern-day hardware, such a programming pattern can
  be used to easily achieve a throughput of thousands of messages a second,

* Again, using pymqi.CMQC.MQGMO_FAIL_IF_QUIESCING is a recommended programming practice.

==========================================
How to specify dynamic reply-to queues
==========================================

Code::

    import pymqi

    queue_manager = 'QM1'
    channel = 'DEV.APP.SVRCONN'
    host = '127.0.0.1'
    port = '1414'
    conn_info = '%s(%s)' % (host, port)
    message = 'Please reply to a dynamic queue, thanks.'
    dynamic_queue_prefix = 'MY.REPLIES.*'
    request_queue = 'TEST.1'

    qmgr = pymqi.connect(queue_manager, channel, conn_info)

    # Dynamic queue's object descriptor.
    dyn_od = pymqi.OD()
    dyn_od.ObjectName = 'SYSTEM.DEFAULT.MODEL.QUEUE'
    dyn_od.DynamicQName = dynamic_queue_prefix

    # Open the dynamic queue.
    dyn_input_open_options = pymqi.CMQC.MQOO_INPUT_EXCLUSIVE
    dyn_queue = pymqi.Queue(qmgr, dyn_od, dyn_input_open_options)
    dyn_queue_name = dyn_od.ObjectName.strip()

    # Prepare a Message Descriptor for the request message.
    md = pymqi.MD()
    md.ReplyToQ = dyn_queue_name

    # Send the message.
    queue = pymqi.Queue(qmgr, request_queue)
    queue.put(message, md)

    # Get and process the response here..

    dyn_queue.close()
    queue.close()
    qmgr.disconnect()


Notes:

* To specify a dynamic reply-to queue, one needs to first create an appropriate
  Object Descriptor and then open the queue, the descriptor's *DynamicQName*
  attribute will be filled in by MQ to the name of a queue created,

* Queue.put accepts a message descriptor on input, its *ReplyToQ* attribute is
  responsible for storing information about where the responding side should
  send the messages to.

==========================================
How to send responses to reply-to queues
==========================================

Code::

    import pymqi

    queue_manager = 'QM1'
    channel = 'DEV.APP.SVRCONN'
    host = '127.0.0.1'
    port = '1414'
    queue_name = 'TEST.1'
    message = 'Here's a reply'
    conn_info = '%s(%s)' % (host, port)

    qmgr = pymqi.connect(queue_manager, channel, conn_info)

    md = pymqi.MD()

    queue = pymqi.Queue(qmgr, queue_name)
    message = queue.get(None, md)

    reply_to_queue_name = md.ReplyToQ.strip()
    reply_to_queue = pymqi.Queue(qmgr, reply_to_queue_name)
    reply_to_queue.put(message)

    queue.close()
    qmgr.disconnect()

Notes:

* Queue.get accepts an input message descriptor parameter, its *ReplyToQ* attribute is
  responsible for storing information about where the responding side should
  send the messages to. The attribute's value is filled in by IBM MQ.


==========================================
How to publish messages on topics
==========================================

Code::

    import pymqi

    queue_manager = 'QM1'
    channel = 'DEV.APP.SVRCONN'
    host = '127.0.0.1'
    port = '1414'
    topic_string = '/currency/rate/EUR/USD'
    msg = '1.3961'
    conn_info = '%s(%s)' % (host, port)

    qmgr = pymqi.QueueManager(None)
    qmgr.connect_tcp_client(queue_manager, pymqi.CD(), channel, conn_info)

    topic = pymqi.Topic(qmgr, topic_string=topic_string)
    topic.open(open_opts=pymqi.CMQC.MQOO_OUTPUT)
    topic.pub(msg)
    topic.close()

    qmgr.disconnect()

Notes:

* pymqi.Topic is a class through which all operations related to MQ topics are
  made,
* a Topic object may be open just like if it were a regular queue,
* once a topic is open, its *.pub* method may be used for publishing the messages.

=================================================================================
How to subscribe to topics (and avoid MQRC_SUB_ALREADY_EXISTS at the same time)
=================================================================================

Code::

    import logging

    import pymqi

    logging.basicConfig(level=logging.INFO)

    queue_manager = 'QM1'
    channel = 'DEV.APP.SVRCONN'
    host = '127.0.0.1'
    port = '1414'
    topic_string = '/currency/rate/EUR/USD'
    msg = '1.3961'
    conn_info = '%s(%s)' % (host, port)

    qmgr = pymqi.QueueManager(None)
    qmgr.connect_tcp_client(queue_manager, pymqi.CD(), channel, conn_info)

    sub_desc = pymqi.SD()
    sub_desc['Options'] = pymqi.CMQC.MQSO_CREATE + pymqi.CMQC.MQSO_RESUME + \
        pymqi.CMQC.MQSO_DURABLE + pymqi.CMQC.MQSO_MANAGED
    sub_desc.set_vs('SubName', 'MySub')
    sub_desc.set_vs('ObjectString', topic_string)

    sub = pymqi.Subscription(qmgr)
    sub.sub(sub_desc=sub_desc)

    get_opts = pymqi.GMO(
        Options=pymqi.CMQC.MQGMO_NO_SYNCPOINT + pymqi.CMQC.MQGMO_FAIL_IF_QUIESCING + pymqi.CMQC.MQGMO_WAIT)
    get_opts['WaitInterval'] = 15000

    data = sub.get(None, pymqi.md(), get_opts)
    logging.info('Here's the received data: [%s]' % data)

    sub.close(sub_close_options=pymqi.CMQC.MQCO_KEEP_SUB, close_sub_queue=True)
    qmgr.disconnect()

Notes:

* A *pymqi.Subscription* and its companion class *pymqi.SD* (a Subscription Descriptor) are
  needed for subscribing to a topic,

* a proper pymqi.SD needs to be created first; note the usage of its *.set_vs* method
  for setting some of the object's properties. It's needed here because parts of
  the pymqi.SD's implementation depend on `ctypes <http://docs.python.org/library/ctypes.html>`_
  and cannot be set directly through the regular dictionary assignment like the 'Options' have been set,

* note well that among other options we're using pymqi.CMQC.MQSO_CREATE + pymqi.CMQC.MQSO_RESUME,
  in plain words in means *create a new subscription of the name set in the
  'SubName' key ('MySub' in the example) but if the subscribtion already exists
  then just resume it*, this basically means we won't stumble upon the
  MQRC_SUB_ALREADY_EXISTS error code,

* once the pymqi.SD has been created, it can be used for subscribing to a particular
  topic with invoking the pymqi.Subscription's *.sub* method,

* once subscribed to the topic, you can use the subscription's *.get* method for
  receiving the messages. Note that the .get method uses regular Get Message Options
  (pymqi.GMO), just like if the subscription was an ordinary queue,

* before disconnecting from the queue manager, a subscription should be closed;
  note passing of the information regarding what MQ should do with the related objects.

.. _ssl_tls:

==========================================
How to use SSL & TLS
==========================================

Code::

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
    qmgr.connect_with_options(queue_manager, cd, sco)

    put_queue = pymqi.Queue(qmgr, queue_name)
    put_queue.put(message)

    get_queue = pymqi.Queue(qmgr, queue_name)
    logging.info('Here is the message again: [%s]' % get_queue.get())

    put_queue.close()
    get_queue.close()
    qmgr.disconnect()


Notes:

* When not using SSL or TLS, PyMQI creates a default *pymqi.CD* object however
  in this case one needs to pass specific SSL/TLS-related information manually
  using *pymqi.CD* and *pymqi.SCO* objects,

* Code above assumes that:

 * Queue manager has been assigned a key repository (SSLKEYR attribute) and
   the repository contains the client's certificate,

 * There is an SVRCONN channel with the following properties set::

        DIS CHANNEL(SSL.SVRCONN.1) SSLCAUTH SSLCIPH
             1 : DIS CHANNEL(SSL.SVRCONN.1) SSLCAUTH SSLCIPH
        AMQ8414: Display Channel details.
           CHANNEL(SSL.SVRCONN.1)                  CHLTYPE(SVRCONN)
           SSLCAUTH(REQUIRED)
           SSLCIPH(TLS_RSA_WITH_AES_256_CBC_SHA)

 * You can access a client key database of type CMS - one, which can be created with gsk6cmd/gsk7cmd tools -
   and there are following files in the /var/mqm/ssl-db/client/ directory (the directory name may
   be arbitrary, /var/mqm/ssl-db/client/ is only an example)::

        $ ls -a /var/mqm/ssl-db/client/
        .  ..  KeyringClient.crl  KeyringClient.kdb  KeyringClient.rdb	KeyringClient.sth
        $

 * The client key database contains a certificate labeled *ibmwebspheremqmy_user*
   and you are running the code as an operating system's account *my_user*,

 * The client key database contains the queue manager's certificate.

* Remember to make sure that:

 * The queue manager certificate's label is prefixed with *ibmwebspheremq* and ends with
   the name of the queue manager, lowercased. If the name of a queue manager is
   QM01 then the label will be *ibmwebspheremqqm01*,

 * The client certificate's label is prefixed with *ibmwebspheremq* and ends with
   the name of the operating system's account under which the code will be executed;
   so if the account name is *user01* then the label will be *ibmwebspheremquser01*,

 * The value of a cd.SSLCipherSpec parameter matches the value of a channel's
   SSLCIPH attribute.

==========================================
How to set and get the message priority
==========================================

Code::

    import logging

    import pymqi

    logging.basicConfig(level=logging.INFO)

    queue_manager = 'QM1'
    channel = 'DEV.APP.SVRCONN'
    host = '127.0.0.1'
    port = '1414'
    queue_name = 'TEST.1'
    message = 'Hello from Python!'
    conn_info = '%s(%s)' % (host, port)
    priority = 2

    put_md = pymqi.MD()
    put_md.Priority = priority

    qmgr = pymqi.connect(queue_manager, channel, conn_info)

    put_queue = pymqi.Queue(qmgr, queue_name)
    put_queue.put(message, put_md)

    get_md = pymqi.MD()
    get_queue = pymqi.Queue(qmgr, queue_name)
    message_body = get_queue.get(None, get_md)

    logging.info('Received a message, priority `%s`.' % get_md.Priority)

    put_queue.close()
    get_queue.close()
    qmgr.disconnect()


Notes:

* Use custom *pymqi.MD* instances for both setting and reading the message priority.

==========================================
How to use channel compression
==========================================

Code::

    import pymqi
    import CMQXC

    queue_manager = 'QM1'
    channel = 'DEV.APP.SVRCONN'
    host = '127.0.0.1'
    port = '1414'
    queue_name = 'TEST.1'
    message = 'Hello from Python!' * 10000
    conn_info = '%s(%s)' % (host, port)

    cd = pymqi.CD()
    cd.MsgCompList[1] = CMQXC.MQCOMPRESS_ZLIBHIGH

    qmgr = pymqi.connect(queue_manager, channel, conn_info)

    queue = pymqi.Queue(qmgr, queue_name)
    queue.put(message)
    queue.close()

    qmgr.disconnect()

Notes:

    * Note that the compression level to use is the second element
      of the cd.MsgCompList list, not the first one,

    * The above assumes the channel's been configured using the following
      MQSC command: *ALTER CHANNEL(SVRCONN.1) CHLTYPE(SVRCONN) COMPMSG(ZLIBHIGH)*

=============================================
How to check completion- and reason codes
=============================================

Code::

    import logging

    import pymqi

    queue_manager = 'QM1'
    channel = 'DEV.APP.SVRCONN'
    host = 'localhost.invalid' # Note the invalid hostname here
    port = '1414'
    conn_info = '%s(%s)' % (host, port)

    try:
        qmgr = pymqi.connect(queue_manager, channel, conn_info)
    except pymqi.MQMIError as e:
        if e.comp == pymqi.CMQC.MQCC_FAILED and e.reason == pymqi.CMQC.MQRC_HOST_NOT_AVAILABLE:
            logging.error('Such a host `%s` does not exist.' % host)

Notes:

* When IBM MQ raises an exception, it is wrapped in a pymqi.MQMIError
  object which exposes 2 useful attributes: *.comp* is a completion code
  and *.reason* is the reason code assigned by MQ. All the completion- and
  reason codes can be looked up in the *pymqi.CMQC* module.

===================================================================
How to check the versions of IBM MQ packages installed, Linux
===================================================================

Code::

    import logging

    import rpm

    logging.basicConfig(level=logging.INFO)

    package_name = 'MQSeriesClient'

    ts = rpm.TransactionSet()
    mi = ts.dbMatch('name', package_name)

    if not mi.count():
        logging.info('Did not find package [%s] in RPM database.' % package_name)
    else:
        for header in mi:
            version = header['version']
            msg = 'Found package `%s`, version `%s`.' % (package_name, version)
            logging.info(msg)

Notes:

* IBM MQ packages for Linux are distributed as RPMs and we can query the
  RPM database for information about what's been installed,

* PyMQI hasn't been used in the example, however the task is related to MQ
  administration and that's why it's been shown here.

=======================================================================
How to check the versions of IBM MQ packages installed, Windows
=======================================================================

Code::

    import logging
    import _winreg

    logging.basicConfig(level=logging.INFO)

    key_name = 'Software\\IBM\\MQSeries\\CurrentVersion'

    try:
        key = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE, key_name)
    except WindowsError:
        logging.info('Could not find IBM MQ-related information in Windows registry.')
    else:
        version = _winreg.QueryValueEx(key, 'VRMF')[0]
        logging.info('IBM MQ version is `%s`.' % version)


* Versions of IBM MQ packages installed under Windows can be extracted
  by querying the Windows registry,

* Again, PyMQI hasn't been used in the example, however the task is related to MQ
  administration and that's why it's been shown here.

=======================================
How to use an alternate user ID
=======================================

Code::

    import pymqi

    queue_manager = 'QM1'
    channel = 'DEV.APP.SVRCONN'
    host = '127.0.0.1'
    port = '1414'
    queue_name = 'TEST.1'
    message = 'Hello from Python!'
    alternate_user_id = 'myuser'
    conn_info = '%s(%s)' % (host, port)

    qmgr = pymqi.connect(queue_manager, channel, conn_info)

    od = pymqi.OD()
    od.ObjectName = queue_name
    od.AlternateUserId = alternate_user_id

    queue = pymqi.Queue(qmgr)
    queue.open(od, pymqi.CMQC.MQOO_OUTPUT | pymqi.CMQC.MQOO_ALTERNATE_USER_AUTHORITY)
    queue.put(message)

    queue.close()
    qmgr.disconnect()


Notes:

* Queue.open accepts an object descriptor (an instance of pymqi.OD class) and
  queue open options, both of which are used here to specify the alternate user ID.

==============================================================================
How to correlate request and response messages using CorrelationId
==============================================================================

(contributed by `Hannes Wagener <https://launchpad.net/~johannes-wagener>`_)

Code::

    # stdlib
    import logging, threading, time, traceback, uuid

    # PyMQI
    import pymqi

    logging.basicConfig(level=logging.INFO)

    # Queue manager name
    qm_name = 'QM1'

    # Listener host and port
    listener = '192.168.1.135(1434)'

    # Channel to transfer data through
    channel = 'DEV.APP.SVRCONN'

    # Request Queue
    request_queue_name = 'REQUEST.QUEUE.1'

    # ReplyTo Queue
    replyto_queue_name = 'REPLYTO.QUEUE.1'

    message_prefix = 'Test Data. '

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
            self.qm.connect_with_options(
                qm_name, opts=pymqi.CMQC.MQCNO_HANDLE_SHARE_NO_BLOCK, cd=cd)

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
                put_mqmd['MsgType'] = pymqi.CMQC.MQMT_REQUEST

                # Set up the ReplyTo QUeue/Queue Manager (Queue Manager is automatically
                # set by MQ).

                put_mqmd['ReplyToQ'] = replyto_queue_name
                put_mqmd['ReplyToQMgr'] = qm_name

                # Set up the put options - must do with NO_SYNCPOINT so that the request
                # message is committed immediately.
                put_opts = pymqi.PMO(Options=pymqi.CMQC.MQPMO_NO_SYNCPOINT + pymqi.CMQC.MQPMO_FAIL_IF_QUIESCING)

                # Create a random message.
                message = message_prefix + uuid.uuid4().hex

                self.req_queue.put(message, put_mqmd, put_opts)
                logging.info('Put request message.  Message: [%s]' % message)

                # Set up message descriptor for get.
                get_mqmd = pymqi.MD()

                # Set the get CorrelId to the put MsgId (which was set by MQ on the put1).
                get_mqmd['CorrelId'] = put_mqmd['MsgId']

                # Set up the get options.
                get_opts = pymqi.GMO(
                    Options=pymqi.CMQC.MQGMO_NO_SYNCPOINT + pymqi.CMQC.MQGMO_FAIL_IF_QUIESCING +
                            pymqi.CMQC.MQGMO_WAIT)

                # Version must be set to 2 to correlate.
                get_opts['Version'] = pymqi.CMQC.MQGMO_VERSION_2

                # Tell MQ that we are matching on CorrelId.
                get_opts['MatchOptions'] = pymqi.CMQC.MQMO_MATCH_CORREL_ID

                # Set the wait timeout of half a second.
                get_opts['WaitInterval'] = 500

                # Open the replyto queue and get response message,
                replyto_queue = pymqi.Queue(self.qm, replyto_queue_name, pymqi.CMQC.MQOO_INPUT_SHARED)
                response_message = replyto_queue.get(None, get_mqmd, get_opts)

                logging.info('Got response message [%s]' % response_message)

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

                    response_message = 'Response to message %s' % request_message
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

Notes:

* The pattern of waiting for response messages by CorrelationId is very common
  and a useful one,
* Requesting application sends a message to the queue and uses the newly
  created put message's MsgId as a parameter for receiving the responses, that is,
  it expectes that in a given period of time there will be a message on the response
  queue whose CorrelationId will be equal to MsgId,
* Responding application receive the requests, copies the MsgId into CorrelationId
  field and sends the response,
* Requesting application receives the response because there was a message with
  the expected CorrelationId.

=======================================
How to avoid MQRC_ALREADY_CONNECTED
=======================================

Code::

    import pymqi

    queue_manager = 'QM1'
    channel = 'DEV.APP.SVRCONN'
    host = '127.0.0.1'
    port = '1414'
    queue_name = 'TEST.1'
    message = 'Hello from Python!'
    conn_info = '%s(%s)' % (host, port)

    cd = pymqi.CD()

    cd.ChannelName = channel
    cd.ConnectionName = conn_info
    cd.ChannelType = pymqi.CMQC.MQCHT_CLNTCONN
    cd.TransportType = pymqi.CMQC.MQXPT_TCP

    connect_options = pymqi.CMQC.MQCNO_HANDLE_SHARE_BLOCK

    qmgr = pymqi.QueueManager(None)

    for x in range(10):
        qmgr.connect_with_options(queue_manager, cd=cd, opts=connect_options)
        qmgr.connect_with_options(queue_manager, cd=cd, opts=connect_options)

    queue = pymqi.Queue(qmgr, queue_name)
    queue.put(message)
    queue.close()

    qmgr.disconnect()

::

    import pymqi

    queue_manager = 'QM1'
    channel = 'DEV.APP.SVRCONN'
    host = '127.0.0.1'
    port = '1414'
    queue_name = 'TEST.1'
    message = 'Hello from Python!'
    conn_info = '%s(%s)' % (host, port)

    qmgr = pymqi.QueueManager(None)
    qmgr.connect_tcp_client(queue_manager, pymqi.CD(), channel, conn_info)

    try:
        qmgr.connect_tcp_client(queue_manager, pymqi.CD(), channel, conn_info)
    except pymqi.MQMIError as e:
        if e.comp == pymqi.CMQC.MQCC_WARNING and e.reason == pymqi.CMQC.MQRC_ALREADY_CONNECTED:
            # Move along, nothing to see here..
            pass

    queue = pymqi.Queue(qmgr, queue_name)
    queue.put(message)
    queue.close()

    qmgr.disconnect()

Notes:

* Two code snippets are copy'and'pastable answers to the question but a discussion
  is in order,

* The first snippet is the recommended way, it tells MQ to reuse a single connection
  regardless of how many times the application will be issuing a request for
  establishing a new connection. That's also a pattern to use when your application
  is multithreaded, without using MQCNO_HANDLE_SHARE_BLOCK MQ would not allow
  the threads to reuse the same connection,

* The second one shows how to ignore the particular exception indicating that
  an application has been already connected.

=======================================
How to define a channel
=======================================

Code::

    import pymqi

    queue_manager = 'QM1'
    channel = 'DEV.APP.SVRCONN'
    host = '127.0.0.1'
    port = '1414'
    conn_info = '%s(%s)' % (host, port)

    channel_name = 'MYCHANNEL.1'
    channel_type = pymqi.CMQXC.MQCHT_SVRCONN

    args = {pymqi.CMQCFC.MQCACH_CHANNEL_NAME: channel_name,
            pymqi.CMQCFC.MQIACH_CHANNEL_TYPE: channel_type}

    qmgr = pymqi.connect(queue_manager, channel, conn_info)

    pcf = pymqi.PCFExecute(qmgr)
    pcf.MQCMD_CREATE_CHANNEL(args)

    qmgr.disconnect()

Notes:

* Instances of *pymqi.PCFExecute* class have direct access to all PCF
  administrative MQ commands. The commands expect a dictionary of parameters
  describing the properties of MQ objects which need to be manipulated. All commands
  and appropriate parameters may be loooked up in modules *pymqi.CMQC*, *pymqi.CMQXC* and *pymqi.CMQCFC*,

* The code above is equivalent to following MQSC command:
  *DEFINE CHANNEL(MYCHANNEL.1) CHLTYPE(SVRCONN)*.

=======================================
How to define a queue
=======================================

Code::

    import pymqi

    queue_manager = 'QM1'
    channel = 'DEV.APP.SVRCONN'
    host = '127.0.0.1'
    port = '1414'
    conn_info = '%s(%s)' % (host, port)

    queue_name = 'MYQUEUE.1'
    queue_type = pymqi.CMQC.MQQT_LOCAL
    max_depth = 123456

    args = {pymqi.CMQC.MQCA_Q_NAME: queue_name,
            pymqi.CMQC.MQIA_Q_TYPE: queue_type,
            pymqi.CMQC.MQIA_MAX_Q_DEPTH: max_depth}

    qmgr = pymqi.connect(queue_manager, channel, conn_info)

    pcf = pymqi.PCFExecute(qmgr)
    pcf.MQCMD_CREATE_Q(args)

    qmgr.disconnect()

Notes:

* Instances of *pymqi.PCFExecute* class have direct access to all PCF
  administrative MQ commands. The commands expect a dictionary of parameters
  describing the properties of MQ objects which need to be manipulated. All commands
  and appropriate parameters may be loooked up in modules *pymqi.CMQC*, *pymqi.CMQXC* and *pymqi.CMQCFC*,

* The code above is equivalent to following MQSC command:
  *DEFINE QLOCAL(MYQUEUE.1) MAXDEPTH(123456)*.

=======================================
How to display channels
=======================================

Code::

    import logging

    import pymqi

    logging.basicConfig(level=logging.INFO)

    queue_manager = 'QM1'
    channel = 'DEV.APP.SVRCONN'
    host = '127.0.0.1'
    port = '1414'
    conn_info = '%s(%s)' % (host, port)

    prefix = 'SYSTEM.*'

    args = {pymqi.CMQCFC.MQCACH_CHANNEL_NAME: prefix}

    qmgr = pymqi.connect(queue_manager, channel, conn_info)
    pcf = pymqi.PCFExecute(qmgr)

    try:
        response = pcf.MQCMD_INQUIRE_CHANNEL(args)
    except pymqi.MQMIError as e:
        if e.comp == pymqi.CMQC.MQCC_FAILED and e.reason == pymqi.CMQC.MQRC_UNKNOWN_OBJECT_NAME:
            logging.info('No channels matched prefix `%s`' % prefix)
        else:
            raise
    else:
        for channel_info in response:
            channel_name = channel_info[CMQCFC.MQCACH_CHANNEL_NAME]
            logging.info('Found channel `%s`' % channel_name)

    qmgr.disconnect()


Notes:

* PCF calls that read MQ objects' definition or status, and MQCMD_INQUIRE_CHANNEL
  among them, return a list of dictionaries, items of which describe the particular
  objects queried for.

* The code above is equivalent to following MQSC command:
  *DIS CHANNEL(SYSTEM.\*)*.

=======================================
How to display queues
=======================================

Code::

    import logging

    import pymqi

    logging.basicConfig(level=logging.INFO)

    queue_manager = 'QM1'
    channel = 'DEV.APP.SVRCONN'
    host = '127.0.0.1'
    port = '1414'
    conn_info = '%s(%s)' % (host, port)

    prefix = 'SYSTEM.*'
    queue_type = pymqi.CMQC.MQQT_MODEL

    args = {pymqi.CMQC.MQCA_Q_NAME: prefix,
            pymqi.CMQC.MQIA_Q_TYPE: queue_type}

    qmgr = pymqi.connect(queue_manager, channel, conn_info)
    pcf = pymqi.PCFExecute(qmgr)

    try:
        response = pcf.MQCMD_INQUIRE_Q(args)
    except pymqi.MQMIError as e:
        if e.comp == pymqi.CMQC.MQCC_FAILED and e.reason == pymqi.CMQC.MQRC_UNKNOWN_OBJECT_NAME:
            logging.info('No queues matched given arguments.')
        else:
            raise
    else:
        for queue_info in response:
            queue_name = queue_info[pymqi.CMQC.MQCA_Q_NAME]
            logging.info('Found queue `%s`' % queue_name)

    qmgr.disconnect()

Notes:

* PCF inquiries, MQCMD_INQUIRE_Q including, return a list of dictionaries,
  items of which describe the particular objects queried for.

* The code above is equivalent to following MQSC command:
  *DIS QMODEL(SYSTEM.\*)*.

=======================================
How to use query filters
=======================================

Code::

    import logging

    import pymqi

    logging.basicConfig(level=logging.INFO)

    qmgr = pymqi.connect(queue_manager, channel, conn_info)
    pcf = pymqi.PCFExecute(qmgr)

    attrs = {
      CMQC.MQCA_Q_NAME :'*',
      CMQC.MQIA_Q_TYPE : CMQC.MQQT_LOCAL,
      CMQCFC.MQIACF_Q_ATTRS : CMQC.MQCA_Q_NAME
    }

    filter1 = pymqi.Filter(CMQC.MQCA_Q_DESC).like('IBM MQ *')
    filter2 = pymqi.Filter(CMQC.MQIA_CURRENT_Q_DEPTH).greater(2)

    result = pcf.MQCMD_INQUIRE_Q(attrs, [f1, f2])

    logging.info('Result is %s', result)

Notes:

* String and integer filters can be applied when looking up MQ objects
* Filters are AND-joined
* In the example above, only queues whose description starts with 'IBM MQ' and whose depth is greater than 2 will be returned

=======================================
How to ping the queue manager
=======================================

Code::

    import pymqi

    queue_manager = 'QM1'
    channel = 'DEV.APP.SVRCONN'
    host = '127.0.0.1'
    port = '1414'
    conn_info = '%s(%s)' % (host, port)

    qmgr = pymqi.connect(queue_manager, channel, conn_info)

    pcf = pymqi.PCFExecute(qmgr)
    pcf.MQCMD_PING_Q_MGR()

    qmgr.disconnect()

Notes:

* Not all PCF commands require input parameters, MQCMD_PING_Q_MGR is one such an
  argument-less command.
