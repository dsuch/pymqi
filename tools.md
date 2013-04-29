
Which MQ versions PyMQI has been tested with?
=============================================

PyMQI 1.3
---------

<table>
    <tr>
        <th>System, architecture and MQ version</th>
        <th>IBM code name</th>
        <th>mqver</th>
    </tr>
    <tr>
        <td>Linux x86, 32-bit, MQ 7.0</td>
        <td>CZJ3YML</td>
        <td></td>
    </tr>
    <tr>
        <td>Linux x86, 64-bit, MQ 7.0</td>
        <td>CZJ3ZML</td>
        <td></td>
    </tr>
    <tr>
        <td>Linux x86, 32-bit, MQ 7.1</td>
        <td>WSMQ_LNX_ON_X86_32_7.1.0.2_EIM</td>
        <td></td>
    </tr>
    <tr>
        <td>Linux x86, 64-bit, MQ 7.1</td>
        <td>WSMQ_LNX_ON_X86_64_7.1.0.2_EIM</td>
        <td></td>
    </tr>
    <tr>
        <td>Linux x86, 32-bit, MQ 7.5</td>
        <td>WS_MQ_LIN_X86_32-BIT_7.5.0.1_EIM</td>
        <td></td>
    </tr>
    <tr>
        <td>Linux x86, 64-bit, MQ 7.5</td>
        <td>WS_MQ_LIN_ON_X86-64_V7.5.0.1_EIM</td>
        <td></td>
    </tr>
</table>

Installing and removing MQ on Ubuntu
====================================

Everything is based on http://www.gefira.pl/blog/2010/07/03/websphere-mq-and-ubuntu-howto/

Prerequisites
-------------

``` bash
sudo apt-get install rpm sharutils
```

<table>
    <tr>
        <td>7.5.0.0 32-bit</td>
        <td>

sudo ./mqlicense.sh -accept && sudo rpm -iavh --nodeps --force-debian \ <br/>
    ./MQSeriesRuntime-7.5.0-0.i386.rpm \ <br/>
    ./MQSeriesJava-7.5.0-0.i386.rpm \ <br/>
    ./MQSeriesClient-7.5.0-0.i386.rpm \ <br/>
    ./MQSeriesServer-7.5.0-0.i386.rpm \ <br/>
    ./MQSeriesSDK-7.5.0-0.i386.rpm \ <br/>
    ./MQSeriesSamples-7.5.0-0.i386.rpm \ <br/>
    ./MQSeriesMan-7.5.0-0.i386.rpm \ <br/>
    && sudo usermod -s /bin/bash mqm
        </td>
</table>
    
    
Removing
--------
sudo rpm -qa | grep "MQSeries" | xargs sudo rpm -e --force-debian --noscripts
sudo rm -rf /opt/mqm
sudo rm -rf /var/mqm
sudo userdel mqm