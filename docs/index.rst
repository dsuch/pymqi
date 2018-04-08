PyMQI
=====

.. note::

    Sponsored by `Zato <https://zato.io/docs?pymqi>`_ - Open-Source ESB, SOA, REST, APIs and Cloud Integrations in Python

Other sections:

.. toctree::
   :maxdepth: 1

   Support <support>
   Examples <examples>

Introduction
============

PyMQI is a production-ready Python extension for IBM's messaging &  queuing middleware,
IBM MQ (formerly know as WebSphere MQ and MQSeries). This allows Python programs to make
calls to connect to queue managers, send messages to, get messages off queues
and issue administrative calls, e.g. to create channels or change queues definitions.

PyMQI has been used in production environments for 10+ years on
Linux, Windows, Solaris and AIX with queue managers running on Linux,
Windows, Solarix, AIX, HP-UX and z/OS mainframe. Supported WebSphere MQ versions are
5.x, 6.x, 7.x, 8.x and 9.x.

PyMQI is released under a MIT-like `Python license <https://github.com/dsuch/pymqi/blob/master/LICENSE>`_.
It's free to use in open-source and proprietary applications.

Here is some minimal code to put a message on a queue::

    import pymqi

    qmgr = pymqi.connect('QM.1', 'SVRCONN.CHANNEL.1', '192.168.1.121(1434)')

    putq = pymqi.Queue(qmgr, 'TESTQ.1')
    putq.put('Hello from Python!')

And here's some more to get it again::

    import pymqi

    qmgr = pymqi.connect('QM.1', 'SVRCONN.CHANNEL.1', '192.168.1.121(1434)')

    getq = pymqi.Queue(qmgr, 'TESTQ.1')
    print('Here is the message:', getq.get())

Installation
============

* As a prerequisite, you first need to install an IBM MQ client in the system that PyMQI is about to be installed
  - it is a free library offered by IBM on top of which higher-level ones, such as PyMQI, can connect to queue managers.
  IBM MQ clients can be downloaded from IBM's website.

* Use pip to install PyMQI itself:

  ::

    $ sudo pip install pymqi


The backbone of IBM MQ Python messaging
========================================

PyMQI is a relatively low-level library that requires one to know IBM APIs fairly well.

It serves, however, as the basis for IBM MQ support in
`Zato <https://zato.io/docs?pymqi>`_,
which is an enterprise API platform and backend application server
in Python that lets one connect to many technologies with little or no programming

This includes IBM MQ queue managers along with ability to seamlessly integrate with Java JMS systems.



.. image:: https://zato.io/support/pymqi/mqdef.png
   :width: 55%

Check out this
`blog post <https://zato.io/blog/posts/websphere-mq-python-zato.html>`_
for an introduction
and visit `Zato documentation <https://zato.io/docs?pymqi>`_ for more information.
