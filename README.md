
# Python library for IBM MQ

PyMQI is a production-ready Python extension for IBM MQ (formerly known as WebSphere MQ and MQSeries),
which for 20+ years has been used by thousands of companies around the world with their queue managers running on
Linux, Windows, UNIX and z/OS.

## Sample code

To put a message on a queue:

```python
import pymqi

queue_manager = pymqi.connect('QM.1', 'SVRCONN.CHANNEL.1', '192.168.1.121(1434)')

q = pymqi.Queue(queue_manager, 'TESTQ.1')
q.put('Hello from Python!')
```

To read the message back from the queue:

```python
import pymqi

queue_manager = pymqi.connect('QM.1', 'SVRCONN.CHANNEL.1', '192.168.1.121(1434)')

q = pymqi.Queue(queue_manager, 'TESTQ.1')
msg = q.get()
print('Here is the message:', msg)
```

## The backbone of IBM MQ Python messaging

PyMQI is a low-level library that requires one to know IBM MQ APIs well.

It serves, however, as the basis for
IBM MQ]
support
in
[Zato](https://zato.io/?gh),
which is an enterprise
API platform and backend application server in Python that lets one connect to many technologies
with little or no programming.

This includes IBM MQ queue managers as well as the ability to seamlessly integrate with Java JMS systems.

![]({{ gfx_prefix }}/api/screenshots/conn1.png)
![]({{ gfx_prefix }}/api/screenshots/mq.png)

## Learn more

Visit the [documentation](https://zato.io/en/docs/3.2/pymqi/index.html?gh) for more information and usage examples.
