
PyMQI - Python interface to IBM MQ (WebSphere MQ, MQSeries)
----------------------------------------------------------

**Sponsored by [Zato](https://zato.io/docs?pymqi-gh01) - ESB, SOA, REST, APIs and Cloud Integrations in Python**

PyMQI allows one to connect to queue managers to issue MQAI and PCF requests.

Consider the code below which establishes a connection, puts a message
on a queue and disconnects.

```python
    import pymqi

    queue_manager = 'QM01'
    channel = 'SVRCONN.1'
    host = '192.168.1.135'
    port = '1434'
    queue_name = 'TEST.1'
    message = 'Hello from Python!'
    conn_info = '%s(%s)' % (host, port)

    qmgr = pymqi.connect(queue_manager, channel, conn_info)

    queue = pymqi.Queue(qmgr, queue_name)
    queue.put(message)
    queue.close()

    qmgr.disconnect()
```

Usage examples
==============

More usage examples can be found here https://dsuch.github.io/pymqi/examples.html

Supported MQ versions
=====================

Any MQ version between 5.0 and 9.0 will work however the author is able to provide
free support only for Linux x86 64-bit, MQ versions 9.x and Python 2.7+.

Support for other versions and systems needs either someone from the commnuity to step up
or contacting the author pymqi@m.zato.io in order to discuss paid support options.

Supported Python versions
=========================

PyMQI will work with:

* Python 2.7
* Python 3.5+

Installation
============

* PyMQI can be installed using pip - downloads are on [PyPI](https://pypi.org/project/pymqi/)

* As a prerequisite, you first need to install an IBM MQ client in the system that PyMQI is about to be installed;
  it is a free library offered by IBM on top of which higher-level ones, such as PyMQI, can connect to queue managers.
  IBM MQ clients can be downloaded from IBM's website.

* Now you can use pip to install PyMQI itself:

```bash
    $ sudo pip install pymqi
```

The backbone of IBM MQ Python messaging
========================================

PyMQI is a relatively low-level library that requires one to know IBM APIs fairly well.

It serves, however, as the basis for IBM MQ support in
[Zato](https://zato.io/docs?pymqi-gh02),
which is an enterprise integration platform and backend application server
in Python that lets one connect to many technologies with little or no programming

This includes IBM MQ queue managers along with ability to seamlessly integrate with Java JMS systems.

![Alt text](https://zato.io/support/pymqi/mqdef.png "Optional title")

Read these
[blog](https://zato.io/blog/posts/python-ibm-mq-part-1.html?pymqi-gh3)
[posts](https://zato.io/blog/posts/websphere-mq-python-zato.html?pymqi-gh4)
for an introduction
and visit [Zato documentation](https://zato.io/docs?pymqi-gh03) for more information.

