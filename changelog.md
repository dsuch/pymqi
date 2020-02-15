PyMQI changelog
---------------

* **1.10.1** (2020-02-15)

  * Added [automatic conversion of Unicode to bytes](https://dsuch.github.io/pymqi/examples.html#sending-unicode-data-vs-bytes)
    in put and put1 operations (thanks [@SeyfSV](https://github.com/SeyfSV) and [@leonjza](https://github.com/leonjza))

* **1.9.3** (2019-12-04)

  * Many thanks to [@SeyfSV](https://github.com/SeyfSV) for contributing the features below
  * Updated MQCD for MQ v9.1.3
  * Changed default values for MQCD.ChannelType and MQCD.TransportType
  * Added MQOpts class for MQXQH header
  * Improvements to the handling of list attributes in MQAI
  * Various changes to string vs. unicode handling in MQ calls

* **1.9.2** (2019-03-12)

  * Added [.get_no_jms](https://dsuch.github.io/pymqi/examples.html#how-to-get-a-message-without-jms-mqrfh2-headers) to return queue messages without JMS/MQRFH2 headers

* **1.9.1** (2019-02-18)

  * Improved installation procedure

* **1.9.0** (2019-02-15)

  * Added support for Mac OS

* **1.8.0** (2018-07-11)

  * Added Python 3 compatibility while still retaining the ability to run under Python 2.6 and 2.7

* **1.7.2** (2018-01-26)

  * Made PCF commands use constants from CMQCFC instead of CMQC

* **1.7.1** (2018-01-24)

  * Internal changes to connect_with_options

* **1.7.0** (2017-12-28)

  * Added MQ 9.0.x compatibility
  * Made remote TCP connections without a queue manager name work

* **1.6.0** (2017-08-09)

  * Made MQSCO compatible with MQ 8.0

* **1.5.4** (2015-09-22)

  * Moved setup.py's py_modules to correct place

* **1.5.3** (2015-09-21)

  * Added missing modules to setup.py

* **1.5.2** (2015-09-21)

  * Previous release failed to upload to PyPI

* **1.5.1** (2015-09-21)

  * Added a missing 'requirements.txt' file

* **1.5** (2015-09-18)

  * Added MQ 8.0.x compatibility
  * Added the ability to connect to MQ 8.0+ queue managers with username/password credentials
  * Moved code to a top-level 'pymqi' package

(No changelog for prior versions)

More information
================

Please visit the main documentation at https://dsuch.github.io/pymqi/ for more information.
