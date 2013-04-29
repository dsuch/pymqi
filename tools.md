
Which MQ versions PyMQI has been tested with?
=============================================

PyMQI 1.3
---------

<table>
    <tr>
        <th>System, architecture and MQ version</th>
        <th>IBM code name</th>
        <th>dspmqver</th>
    </tr>
    <tr>
        <td>Linux x86, 64-bit, MQ 7.0</td>
        <td>CZJ3ZML</td>
        <td></td>
    </tr>
    <tr>
        <td>Linux x86, 64-bit, MQ 7.1</td>
        <td>WSMQ_LNX_ON_X86_64_7.1.0.2_EIM</td>
        <td>
Name:        WebSphere MQ <br/>
Version:     7.1.0.2 <br/>
Level:       p710-002-121029 <br/>
BuildType:   IKAP - (Production) <br/>
Platform:    WebSphere MQ for Linux (x86-64 platform) <br/>
Mode:        64-bit <br/>
O/S:         Linux 3.2.0-40-generic <br/>
InstName:    Installation1 <br/>
InstDesc:     <br/>
InstPath:    /opt/mqm <br/>
DataPath:    /var/mqm <br/>
Primary:     No <br/>
MaxCmdLevel: 711
        </td>
    </tr>
    <tr>
        <td>Linux x86, 64-bit, MQ 7.5</td>
        <td>WS_MQ_LIN_ON_X86-64_V7.5.0.1_EIM</td>
        <td>
Name:        WebSphere MQ <br/>
Version:     7.5.0.0 <br/>
Level:       p000-L120604 <br/>
BuildType:   IKAP - (Production) <br/>
Platform:    WebSphere MQ for Linux (x86-64 platform) <br/>
Mode:        64-bit <br/>
O/S:         Linux 3.2.0-40-generic <br/>
InstName:    Installation1 <br/>
InstDesc:     <br/>
InstPath:    /opt/mqm <br/>
DataPath:    /var/mqm <br/>
Primary:     No <br/>
MaxCmdLevel: 750
        </td>
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
        <td>7.1 64-bit</td>
        <td>

sudo ./mqlicense.sh -accept && sudo rpm -iavh --nodeps --force-debian \ <br/>
    ./MQSeriesRuntime-7.1.0-2.x86_64.rpm \ <br/>
    ./MQSeriesJava-7.1.0-2.x86_64.rpm \ <br/>
    ./MQSeriesClient-7.1.0-2.x86_64.rpm \ <br/>
    ./MQSeriesServer-7.1.0-2.x86_64.rpm \ <br/>
    ./MQSeriesSDK-7.1.0-2.x86_64.rpm \ <br/>
    ./MQSeriesSamples-7.1.0-2.x86_64.rpm \ <br/>
    ./MQSeriesMan-7.1.0-2.x86_64.rpm \ <br/>
    && sudo usermod -s /bin/bash mqm
        </td>
    </tr>
    <tr>
        <td>7.5 64-bit</td>
        <td>

sudo ./mqlicense.sh -accept && sudo rpm -iavh --nodeps --force-debian \ <br/>
    ./MQSeriesRuntime-7.1.0-2.x86_64.rpm  \ <br/>
    ./MQSeriesJava-7.1.0-2.x86_64.rpm  \ <br/>
    ./MQSeriesClient-7.1.0-2.x86_64.rpm  \ <br/>
    ./MQSeriesServer-7.1.0-2.x86_64.rpm  \ <br/>
    ./MQSeriesSDK-7.1.0-2.x86_64.rpm  \ <br/>
    ./MQSeriesSamples-7.1.0-2.x86_64.rpm  \ <br/>
    ./MQSeriesMan-7.1.0-2.x86_64.rpm  \ <br/>
    && sudo usermod -s /bin/bash mqm
        </td>
    </tr>
</table>

Test environment
----------------

(As user mqm)

``` bash
/opt/mqm/bin/crtmqm QM01
/opt/mqm/bin/strmqm QM01

echo "define qlocal(q1)" > commands.in
echo "define channel(svrconn.1) chltype(svrconn) mcauser('mqm')" >> commands.in # Note mcauser!
echo "alter qmgr chlauth(disabled)" >> commands.in # Dangerous!
/opt/mqm/bin/runmqsc QM01 < commands.in

/opt/mqm/bin/runmqlsr -m QM01 -t tcp -p 1434 &
```

Removing
--------

(First stop the queue manager and runmqlsr listener)

``` bash
sudo rpm -qa | grep "MQSeries" | xargs sudo rpm -e --force-debian --noscripts
sudo rm -rf /opt/mqm
sudo rm -rf /var/mqm
sudo userdel mqm
```