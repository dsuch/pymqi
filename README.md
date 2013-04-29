
PyMQI - Python interface to WebSphere MQ (MQSeries)
-------------------------------------------------------

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


More usage examples can be found here https://pythonhosted.org/pymqi/examples.html

Supported MQ versions
=====================

Any MQ version between 5.0 and 7.5 will work however the author is able to provide
free support only for Linux x86 64-bit and MQ versions 7.x.

Support for other versions and systems needs either someone from the commnuity to step up
or contacting the author dsuch@gefira.pl in order to discuss paid support options.

Download
========

Downloads are hosted on PyPI https://pypi.python.org/pypi/pymqi

More information
================

Please visit the main documentation at https://pythonhosted.org/pymqi/index.html for more information.
