
# Python library for IBM MQ

PyMQI is a production-ready, open-source Python extension for IBM MQ (formerly known as WebSphere MQ and MQSeries).

For 20+ years, the library has been used by thousands of companies around the world with their queue managers running on
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

If you'd like to have an easy to use IBM MQ interface that doesn't require an extensive knowledge of MQ,
use
[Zato],
which is a Python-based
[IPaaS](https://zato.io/articles/integration-platform.html)
and
[enterprise service bus](https://zato.io/en/docs/3.3/intro/esb-soa.html)
that supports MQ, among other protocols.

This includes IBM MQ queue managers as well as the ability to seamlessly integrate with Java JMS systems.

![](https://upcdn.io/kW15bqq/raw/root/en/docs/3.3/gfx/api/screenshots/mq.png)

## Learn more

Visit the [documentation](https://zato.io/pymqi/index.html?gh) for more information and usage examples.
