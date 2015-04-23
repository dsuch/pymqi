.. PyMQI documentation master file, created by
   sphinx-quickstart on Tue Oct  6 13:12:00 2009.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

PyMQI 1.4 Documentation
=================================

Other sections:

.. toctree::
   :maxdepth: 1

   Support, consulting and contact <support-consulting-contact>
   Examples <examples>
   Notes on building PyMQI on Windows <mingw32>
   API Docs <api>

=================
Introduction
=================

PyMQI is a production-ready Python extension for IBM's messaging & queueing middleware,
WebSphere MQ (formerly know as MQSeries). This allows Python programs to make
calls directly to MQI to connect queues and get/put messages on them etc.

PyMQI combines the power of Python with the benefits of the messaging model.
It can be used to develop test harnesses for MQ based systems, for rapid
prototyping of MQ applications, for development of administrative GUIs
or for mainstream MQ application development!

PyMQI does not replace MQI, but is layered on top of it, so you must have
MQ (either client or server) installed before you can use PyMQI.

PyMQI has been used in production environments for several years on
Linux, Windows, Solaris and AIX with queue managers running on Linux,
Windows, Solarix, AIX, HP-UX and z/OS mainframe. Supported WebSphere MQ versions are
5.x, 6.x and 7.x.

PyMQI consists of several modules that are used together:

    * CMQC, CMQXC, CMQCFC, CMQZC define all the constants for MQI.
    * pymqe a low-level Python extension interface to MQI, written in C.
    * pymqi a high-level Python OO interface to MQI that uses pymqe.

It's easiest to use the pymqi package. Here is some minimal code to put a message on a queue::

    import pymqi

    qmgr = pymqi.connect('QM.1', 'SVRCONN.CHANNEL.1', '192.168.1.121(1434)')

    putq = pymqi.Queue(qmgr, 'TESTQ.1')
    putq.put('Hello from Python!')

And here's some more to get it again::

    import pymqi

    qmgr = pymqi.connect('QM.1', 'SVRCONN.CHANNEL.1', '192.168.1.121(1434)')

    getq = pymqi.Queue(qmgr, 'TESTQ.1')
    print("Here's the message:", getq.get())

Easy, eh?

For the MQI calls that PyMQI supports, the full set of options are implemented.
This allows you access to the full functionality of the MQI call from Python.
PyMQI defines classes that are synonymous with the MQI structure parameters,
such as MQGMO, MQPMO etc. This lets you program MQI 'the Python way'.

.. _download_build_install:

=========================
Download, build & install
=========================

Automated install using pip
---------------------------

On Linux and UNIX one can use `pip <https://pypi.python.org/pypi/pip>`_
- PyMQI is a Python package and as such can be installed 
using pip, which is a specialized installer for Python applications. pip will 
connect to PyPI which is a central repository of Python packages, available 
at https://pypi.python.org/pypi and will then look up PyMQI, download it 
from https://pypi.python.org/pypi/pymqi and install it locally on your system.

First you need to install pip itself.

On most Linux systems the package pip is in is called 'pip' or 'pip-python'
so - depending on your distribution - you can simply issue one of the commands 
below to get it installed::
  
  $ sudo apt-get install pip
  # yum install pip
  # zypper in python-pip
  
Assuming you have root power, you can now install PyMQI system-wide using the 
command below - again, adjust the 'pip' command name for your particular system,
it usually is 'pip' can be 'pip-python' sometimes::

  $ sudo pip install pymqi
  
Or, if you don't have root access, you can install PyMQI for a particular user
only (this will be installed to $HOME/.local)::

  $ pip install --user pymqi

Compiling from source
---------------------
`Download the latest version here <https://pypi.python.org/pypi/pymqi>`_.
The download package is a source
distribution with a Distutils setup.py file. Download, unzip & untar the
file, then cd into the pymqi directory. Note that compiling from source needs access
to Python development headers - such as Python.h - on Linux it means you first
need to install the development DEB or RPM package, typically called *python-dev*
or similarly.

PyMQI may be built in both client and server mode. The client mode requires one
to connect to queue managers through a SVRCONN MQ channel. The server mode allows
for connecting in MQ bindings mode. **If you're unsure which one to choose, build PyMQI
in a client mode**.

Here's the step of actions for building and installing an MQI PyMQI client::

    $ python setup.py build client
    $ python setup.py install

And here's how to build and install PyMQI in a server mode::

    $ python setup.py build server
    $ python setup.py install

If you are building PyMQI on Windows and you don't have MSVC installed,
you can use MinGW instead. Jaco Smuts has written notes `here <mingw32.html>`_ explaining
how itis done.

`See this StackOverflow post if you're compiling on AIX 
<http://stackoverflow.com/questions/5376514/how-do-i-force-python-pymqi-1-2-to-use-my-gcc-compiler-when-i-build-it>`_ 
and would like to force PyMQI to use GCC instead of cc_r.

If you port PyMQI to other platforms, `please let me know <support-consulting-contact.html>`_.

=========================
Supported Functionality
=========================

The following MQI calls are supported.

    * MQCONN, MQDISC
    * MQCONNX
    * MQOPEN/MQCLOSE
    * MQPUT/MQPUT1/MQGET
    * MQCMIT/MQBACK
    * MQBEGIN
    * MQINQ
    * MQSET
    * MQSUB
    * MQCRTMH
    * MQSETMP
    * MQINQMP
    * And various MQAI PCF commands.

In support of these, PyMQI implements the following structures. Others
will follow to support additional MQI calls as required.

    * MQCD
    * MQCMHO
    * MQMD
    * MQGMO
    * MQIMPO
    * MQOD
    * MQPD
    * MQPMO
    * MQRFH2
    * MQSCO
    * MQSMPO
    * MQSRO
    * MQSD
    * MQTM
    * MQTMC2

For a client build, pymqi.__mqbuild__ is set to the string 'client',
otherwise it is set to 'server'. The supported command levels
(from 5.0 onwards) for the version of MQI linked with PyMQI are available
in the tuple pymqi.__mqlevels__. To determine if a particular level is
supported, do something like::


        if '7.0' in pymqi.__mqlevels__:
            print('New MQI things to try!')

===========
Platforms
===========

PyMQI is known to work on Linux, Windows, Solaris and AIX.  It ought to build
& work on any 32-bit or 64-bit platform that supports MQI & Python. It has been
used with queue managers running on Linux, Windows, Solaris, AIX, HP-UX and z/OS
mainframe.

If you port PyMQI to other platforms and would like to contribute your
changes, `please contact the author <support-consulting-contact.html>`_.

===============
PCF Interface
===============

PyMQI supports Programmable Command Format (PCF) if built with MQ version
5.3 or newer. This allows you to easily administer and configure MQ. The full set
of PCF commands is available.

To use PCF with PyMQI, instantiate a PFCExecute passing it a QueueManager object.
Then call a PCF command, passing a dictionary of attributes
and values, as appropriate to the command. Commands and attributes are as
defined by IBM in cmqc.h, cmqcfc.h, and in their documentation.

You can also use PCF to query a queue manager. In this case, PCFExecute
returns a list of dictionaries, with the attributes and values you have
requested.

An example PCFExecute usage is given below::

        import pymqi, CMQC
        from CMQCFC import *

        qmgr = pymqi.connect('QM.1', 'SVRCONN.CHANNEL.1', '192.168.1.121(1434)')
        pcf = pymqi.PCFExecute(qmgr)

        # Ping the queue manager
        pcf.MQCMD_PING_Q_MGR()

        # Create a channel "SVRCONN.CHANNEL.2"
        chanArgs = {MQCACH_CHANNEL_NAME : "SVRCONN.CHANNEL.2",
                    MQIACH_CHANNEL_TYPE : CMQC.MQCHT_RECEIVER}
        pcf.MQCMD_CREATE_CHANNEL(chanArgs)

        # Query all queues beginning with "TESTQ"
        queues = pcf.MQCMD_INQUIRE_Q({CMQC.MQCA_Q_NAME : "TESTQ*"})
        for q in queues:
            print(pcf.stringify_keys(q))

======================================================
MQBEGIN, Distributed Transactions, XA and all that
======================================================

The use of QueueManager.begin() allows a PyMQI application to coordinate
distributed transactions. This means that updates to queues & databases
(or anything else supported by the XA interface) are linked. If a queue
get/put fails, any database updates within the transaction are backed out.
Similarly, if a database update fails, any queue get/put operations within
the transaction are undone.

This depends on the MQ Transaction Manager, which in turn coordinates
resources through the XA interface. To make this work from Python, you must
use an XA enabled database API. The only one I'm aware of that works is
DCOracle2. You will need to apply `these (unofficial) patches <dco2patch>`_.

You will also have to configure the Queue Manager with XA information for
the resources you want it to coordinate. See the MQSeries System
Administration book for more details.

You might also be interested in a Python extension for the XA Switch
interface. This lets Python applications participate directly in the Distributed
Transaction two phase commit protocol. `See here <pyxasw.tar.gz>`_ for more details.
Pyxasw & PyMQI are related but independent of each other.

This code fragment shows a transactional MQ put & DCO2 database insert,
coordinated by MQ::


        import pymqi, DCOracle2

        qmgr = pymqi.QueueManager()
        q = pymqi.Queue(qmgr, 'TESTQ1')
        pmo = pymqi.PMO(Options = CMQC.MQPMO_SYNCPOINT)
        md = pymqi.MD()

        # Begin a global transaction
        qm.begin()

        # Connect a XA managed database
        conn=DCOracle2.connectXA()
        curs = conn.cursor()

        # Do a transactional put & db insert
        q.put('TM comes to Linux!', md, pmo)
        curs.execute("INSERT INTO TESTTABLE VALUES(42, 'Lala')")

        # Now commit the transaction
        qmgr.commit()


================
Inquire & Set
================
PyMQI supports a simple yet powerful interface to the MQI MQINQ & MQSET calls.

The QueueManager.inquire() and Queue.inquire() calls allow you to inquire
on a single MQ attribute. An integer or string attribute value is returned,
as appropriate.

The Queue.set() call lets you set a single Queue attribute. The value passed
must be of the appropriate type.

When inquiring or setting on a queue, the queue must be specifically opened
for inquire or set. The operations cannot be mixed on a queue, neither can
a get/put queue be used for inquire or set. No such restriction applies to
QueueManager objects.

An example inquire is shown below::


    import pymqi, CMQC

    qmgr = pymqi.connect('QM.1', 'SVRCONN.CHANNEL.1', '192.168.1.121(1434)')

    q = pymqi.Queue(qmgr, 'TESTQ.1')

    print('Queue depth:', q.inquire(CMQC.MQIA_CURRENT_Q_DEPTH))
    print('Queue Manager platform:', qmgr.inquire(CMQC.MQIA_PLATFORM))

================
SSL & TLS
================

PyMQI supports encrypted SSL & TLS connections right out of the box,
see :ref:`here <ssl_tls>` for the usage example.

==========================
PEP-8 API transition plan
==========================

Starting with PyMQI 1.2, the API will be transitioned towards the
`PEP-8 <http://www.python.org/dev/peps/pep-0008/>`_ compliance.
If you're new to PyMQI and have never used versions older than 1.2 then you have
absolutely nothing to do on your end. If however there's already some code of yours
that has been written using the pre-1.2 API then read on.

Using the Python's built-in facilities, some of the classes and methods will be
gradually declared deprecated and you'll be encouraged to use new names instead
of the old ones.

The affected API has been listed below:

=======================================  ========================================
PyMQI < 1.2                              PyMQI 1.2+
=======================================  ========================================
pymqi.gmo                                pymqi.GMO
pymqi.pmo                                pymqi.PMO
pymqi.od                                 pymqi.OD
pymqi.md                                 pymqi.MD
pymqi.cd                                 pymqi.CD
pymqi.sco                                pymqi.SCO
pymqi.QueueManager.connectWithOptions    pymqi.QueueManager.connect_with_options
pymqi.QueueManager.connectTCPClient      pymqi.QueueManager.connect_tcp_client
pymqi.QueueManager.getHandle             pymqi.QueueManager.get_handle
pymqi.PCFExecute.stringifyKeys           pymqi.PCFExecute.stringify_keys
=======================================  ========================================

How does it work precisely?

=======================================  ========================================
Planned date                             Planned action
=======================================  ========================================
March 2011                               The PEP-8 compliant API has been introduced and it's been aliased to the old one, there's no difference in using either one however you're *strongly* encouraged to use only the new one in new code. (*done in PyMQI 1.2*)
October 2012                             Using the old API will issue a `PendingDeprecationWarning <http://docs.python.org/library/exceptions.html#exceptions.PendingDeprecationWarning>`_  in run-time
March 2014                               Using the old API will issue a `DeprecationWarning <http://docs.python.org/library/exceptions.html#exceptions.DeprecationWarning>`_  in run-time
October 2015                             Using the old API will raise a run-time exception making it effectively impossible to use the old API
=======================================  ========================================

In short, the old API will work until October 2015 but given the idea of issuing
warnings, you'd be better off preparing for the new API as soon as possible.

============
Uninstalling
============

Uninstalling PyMQI is a matter of removing the files on disk, for instance,
under Ubuntu, when using Python 2.6, the following commands may be used::

    $ sudo rm /usr/local/lib/python2.6/dist-packages/CMQ*.py*
    $ sudo rm /usr/local/lib/python2.6/dist-packages/pymq*.*

That is, all PyMQI-related files always match one of the patterns, either CMQ*.py*
or pymq*.*

==========
FAQ
==========
1. Why can't I connect PyMQI to the queue manager?

    If you see this error::

        pymqi.MQMIError: MQI Error. Comp: 2, Reason 2058: FAILED: MQRC_Q_MGR_NAME_ERROR

    And you're certain the queue manager is running, then you're probably
    running in an MQ client environment without telling PyMQI where the server is.
    If you don't know the difference between an MQ client and server, please read
    the IBM documentation.

    The answer is to either:

    Set the MQSERVER environment variable to something like "SYSTEM.DEF.SVRCONN/TCP/192.168.1.24(1414)" (or whatever your MQ Server channel/address is).

    Pass in all the connection options to *pymqi.connect*, as in::

        qmgr = pymqi.connect('test.queue.manager', 'SYSTEM.DEF.SVRCONN', '192.168.1.24(1414)'))

    If it still doesn't work, then you've probably built PyMQI against
    the MQ server library rather than the client.

===================
Caveats
===================

    * If a MQI message is truncated, a .get call will raise an exception and you
      will not be able to access the partially received message. This is bad news
      if you're using MQGMO_ACCEPT_TRUNCATED_MSG, as the message will be lost for
      good. The workaround is to let PyMQI allocate the buffer for you, or specify
      a big enough buffer, or stop accepting truncated messages. The latter options
      don't work too well, as you can't find out how big the actual message is!

    * PyMQI unpacks the the MsgId and CorrelId fields of the MQMD structure as a
      '24s', regardless of what you put in it. This leads to some asymmetry when
      sending integers with these field. e.g., On the put side::

              md.MsgId = struct.pack('l', 42)

      And on the get side::

              msgId = struct.upack('l', md.MsgId[0:4])[0]


===============
Sample code
===============

See :doc:`here <examples>` for sample code and examples.

=====================
More documentation
=====================
The author's blog:

    * `WebSphere MQ Administration with Python. Part I – introducing PCFExecute <http://www.zato.io/blog/2011/03/10/websphere-mq-administration-with-python-part-i-introducing-pcfexecute/>`_ (March 10th, 2011)
    * `Message browsing with WebSphere MQ and PyMQI <http://www.zato.io/blog/2011/02/21/message-browsing-with-websphere-mq-and-pymqi/>`_ (February 21st, 2011)
    * `A quick intro to WebSphere MQ & Python programming <http://www.zato.io/blog/2011/01/31/a-quick-intro-to-websphere-mq-python-programming/>`_ (January 31st, 2011)
    * `PyMQI 1.2 is coming soon <http://www.zato.io/blog/2010/12/03/pymqi-1-2-is-coming-soon/>`_ (December 3rd, 2010)
    * `PyMQI 1.0 – Python i WebSphere MQ <http://www.zato.io/blog/2009/12/05/pymqi-1-0-python-i-websphere-mq/>`_ (Polish only,  December 5th, 2009)

Other documentation:

    * `Installing PyMQI 1.2 on CentOS 5.5 <http://nsupathy.wordpress.com/2011/03/22/installing-pymqi1-2-on-centos-5-5/>`_ at Umapathy's Blog (March 22, 2011)
    * Sami Salkosuo of IBM has written `a developerWorks article about PyMQI here <http://www.ibm.com/developerworks/websphere/library/techarticles/0708_salkosuo/0708_salkosuo.html>`_. It gives a good overview and includes several good example applications (August 29th, 2007)
    * PyMQI has plenty of doc strings. They're `reproduced here <api.html>`_ for convenience.


======================
Acknowledgments
======================

**Les Smithson** is the original author and maintainer of PyMQI. Les is available
for Python, MQ, Linux/Unix & C/C++ consulting assignments.
`See here for his CV and more details <http://www.open-networks.co.uk>`_.

Thanks to the following (in no particular order) for their code, suggestions,
ports, bug-fixes etc.

    * Pascal Gauthier
    * John Kittel
    * Yves Lepage
    * John OSullivan
    * Tim Couper
    * Maas-Maarten Zeeman
    * Rich LaMarche
    * Kevin Kalbfleisch
    * Mauricio Strello
    * Brian Vicente
    * Jaco Smuts
    * Brent S. Elmer, Ph.D.
    * Hannes Wagener
    * Andy Piper

================
Related projects
================

    * `Spring Python <http://springpython.webfactional.com/>`_ uses PyMQI in `its implementation of JMS <http://static.springsource.org/spring-python/1.2.x/sphinx/html/jms.html>`_. If you need to seamingly exchange messages
      between Python and Java MQ applications then Spring Python is the project to use as it brings
      the world of JMS WebSphere MQ programming to Python.

================
Disclaimer
================

You are free to use this code in any way you like, subject to the Python
& IBM disclaimers & copyrights. I make no representations about the suitability
of this software for any purpose. It is provided "AS-IS" without warranty
of any kind, either express or implied. So there.

===============
Donate
===============
.. image:: http://images.sourceforge.net/images/project-support.jpg

`Donate to PyMQI <http://sourceforge.net/donate/index.php?group_id=12210>`_

