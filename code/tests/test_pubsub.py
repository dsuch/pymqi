#! /apps/prod/current/bin/python2.7
# -*- coding: iso-8859-15 -*-

import config
import pymqi
import sys
import unittest
import time
import unicodedata


def py23byte(s):
    if isinstance(s, str) and not isinstance(s, bytes):
        return s.encode('utf-8')


class TestPubSub(unittest.TestCase):
    """Test Pub/Sub with the following six test cases:
    |-------+---------+-------------+----------+-------------|
    |       | Managed | Managed     | Provided | Provided    |
    |       | Durable | Non-Durable | Durable  | Non-Durable |
    |-------+---------+-------------+----------+-------------|
    | Admin | x       |             | x        |             |
    | API   | x       | x           | x        | x           |
    |-------+---------+-------------+----------+-------------|
    The combination Admin/Non-Durable is not possible.
    All tests follow the same procedure:
    1. Create or register the subscription
    2. Publish a message
    3. get() the message
    4. compare result with message
    5. tearDown(): delete objects
    """
    def setUp(self):
        self.topic_string_template = "/UNITTEST/{prefix}/PUBSUB/{{type}}/{{destination}}/{{durable}}".format(
            prefix=config.MQ.QUEUE.PREFIX)
        self.subname_template = "{prefix}'s {{type}} {{destination}} {{durable}} Subscription".format(
            prefix=config.MQ.QUEUE.PREFIX)
        self.msg_template = "Hello World in the topic string \"{{topic_string}}\"".format()
        # max length of queue names is 48 characters
        self.queue_name_template = "{prefix}_Q_TEST_PUBSUB_{{type}}_PROVIDED_{{durable}}".format(prefix=config.MQ.QUEUE.PREFIX)
        self.queue_manager = config.MQ.QM.NAME
        self.channel = config.MQ.QM.CHANNEL
        self.host = config.MQ.QM.HOST
        self.port = config.MQ.QM.PORT
        self.user = config.MQ.QM.USER
        self.password = config.MQ.QM.PASSWORD

        self.conn_info = "{0}({1})".format(self.host, self.port)

        self.qmgr = pymqi.QueueManager(None)
        self.qmgr.connectTCPClient(self.queue_manager, pymqi.CD(), self.channel, self.conn_info, self.user, self.password)

        # list of tuples (subscription, subscription descriptions) for tearDown() to delete after the test
        self.sub_desc_list = []

    def delete_sub(self, sub_desc):
        # can only delete a durable subscription
        if sub_desc["Options"] & pymqi.CMQC.MQSO_DURABLE:
            subname = sub_desc.get_vs("SubName")
            pcf = pymqi.PCFExecute(self.qmgr)
            args= { pymqi.CMQCFC.MQCACF_SUB_NAME : subname
                    }
            pcf.MQCMD_DELETE_SUBSCRIPTION(args)

    def delete_queue(self, sub_desc, queue_name):
        # must be unmanaged
        if not sub_desc["Options"] & pymqi.CMQC.MQSO_MANAGED:
            pcf = pymqi.PCFExecute(self.qmgr)
            args = { pymqi.CMQC.MQCA_Q_NAME : queue_name,
                     pymqi.CMQCFC.MQIACF_PURGE : pymqi.CMQCFC.MQPO_YES }
            pcf.MQCMD_DELETE_Q(args)

    def tearDown(self):
        """Delete the created objects.
        """
        for (sub, sub_desc, queue_name) in self.sub_desc_list:
            self.delete_sub(sub_desc)
            if queue_name is None:
                sub_queue = sub.get_sub_queue()
                self.delete_queue(sub_desc, sub_queue)
            else:
                self.delete_queue(sub_desc, queue_name)
        self.qmgr.disconnect()

    def get_subscription_descriptor(self, subname, topic_string, options=0):
        sub_desc = pymqi.SD()
        sub_desc["Options"] = options
        sub_desc.set_vs("SubName", subname)
        sub_desc.set_vs("ObjectString", topic_string)
        return sub_desc

    def pub(self, msg, topic_string, *opts):
        topic = pymqi.Topic(self.qmgr, topic_string=topic_string)
        topic.open(open_opts=pymqi.CMQC.MQOO_OUTPUT)
        if isinstance(msg, str) and not isinstance(msg, bytes):
            msg = msg.encode('utf-8')  # py3
        topic.pub(msg, *opts)
        topic.close()

    def create_api_subscription(self):
        return pymqi.Subscription(self.qmgr)

    def create_admin_subscription(self, destination_class, subname, queue_name, topic_string):
        pcf = pymqi.PCFExecute(self.qmgr)
        args = { pymqi.CMQCFC.MQCACF_SUB_NAME : subname,
                 pymqi.CMQC.MQCA_TOPIC_STRING: topic_string,
                 pymqi.CMQCFC.MQIACF_DESTINATION_CLASS: destination_class }
        if destination_class is pymqi.CMQC.MQDC_PROVIDED:
                 args[pymqi.CMQCFC.MQCACF_DESTINATION] = queue_name
        pcf.MQCMD_CREATE_SUBSCRIPTION(args)

    def create_get_opts(self):
        get_opts = pymqi.GMO(
            Options=pymqi.CMQC.MQGMO_NO_SYNCPOINT + pymqi.CMQC.MQGMO_FAIL_IF_QUIESCING + \
                pymqi.CMQC.MQGMO_WAIT)
        get_opts["WaitInterval"] = 15000
        return get_opts

    def create_queue(self, queue_name):
        queue_type = pymqi.CMQC.MQQT_LOCAL
        max_depth = 123456

        args = { pymqi.CMQC.MQCA_Q_NAME: queue_name,
                 pymqi.CMQC.MQIA_Q_TYPE: queue_type,
                 pymqi.CMQC.MQIA_MAX_Q_DEPTH: max_depth }
        pcf = pymqi.PCFExecute(self.qmgr)
        pcf.MQCMD_CREATE_Q(args)


############################################################################
#
# Real Tests start here
#
############################################################################

    def test_pubsub_api_managed_durable(self):
        topic_string = py23byte(self.topic_string_template.format(type="API", destination="MANAGED", durable="DURABLE"))
        subname = py23byte(self.subname_template.format(type="Api", destination="Managed", durable="Durable"))
        msg = py23byte(self.msg_template.format(topic_string=topic_string))
        # register Subscription
        sub = self.create_api_subscription()

        # define a list self.sub_desc_list of subscription definitions so tearDown() can find it
        sub_desc = self.get_subscription_descriptor(subname, topic_string,
                        pymqi.CMQC.MQSO_CREATE + pymqi.CMQC.MQSO_DURABLE + pymqi.CMQC.MQSO_MANAGED)
        self.sub_desc_list = [(sub, sub_desc, None)]

        sub.sub(sub_desc=sub_desc)
        # publish (put)
        self.pub(msg, topic_string)
        get_opts = self.create_get_opts()
        data = sub.get(None, pymqi.md(), get_opts)
        sub.close(sub_close_options=0, close_sub_queue=True)
        self.assertEqual(data, msg)

    def test_pubsub_api_managed_durable_1_to_n(self):
        """Test multiple subscriptions."""
        # number of subscriptions
        nsub = 5
        topic_string = py23byte(self.topic_string_template.format(type="API", destination="MANAGED", durable="DURABLE"))
        subname = py23byte(self.subname_template.format(type="Api", destination="Managed", durable="Durable"))
        msg = py23byte(self.msg_template.format(topic_string=topic_string))
        self.sub_desc_list = []
        subscriptions = []
        for n in range(nsub):
            sub_desc = self.get_subscription_descriptor(
                self.subname_template.format(type="Api", destination="Managed", durable="Durable{0}".format(n)),
                self.topic_string_template.format(type="API", destination="MANAGED", durable="DURABLE"),
                pymqi.CMQC.MQSO_CREATE + pymqi.CMQC.MQSO_DURABLE + pymqi.CMQC.MQSO_MANAGED)
            # register Subscription
            sub = self.create_api_subscription()
            self.sub_desc_list.append((sub, sub_desc, None))
            sub.sub(sub_desc=sub_desc)
            subscriptions.append(sub)
        
        # publish (put)
        self.pub(msg, topic_string)

        get_opts = self.create_get_opts()
        for n in range(nsub):
            data = subscriptions[n].get(None, pymqi.md(), get_opts)
            subscriptions[n].close(sub_close_options=0, close_sub_queue=True)
            self.assertEqual(data, msg)

    def test_pubsub_api_managed_non_durable(self):
        topic_string = py23byte(self.topic_string_template.format(type="API", destination="MANAGED", durable="NON DURABLE"))
        subname = py23byte(self.subname_template.format(type="Api", destination="Managed", durable="Non Durable"))
        msg = py23byte(self.msg_template.format(topic_string=topic_string))
        sub_desc = self.get_subscription_descriptor(subname, topic_string,
                                                    pymqi.CMQC.MQSO_CREATE + pymqi.CMQC.MQSO_MANAGED)
        # register Subscription
        sub = self.create_api_subscription()
        self.sub_desc_list = [(sub, sub_desc, None)]
        sub.sub(sub_desc=sub_desc)
        # publish (put)
        self.pub(msg, topic_string)
        get_opts = self.create_get_opts()
        data = sub.get(None, pymqi.md(), get_opts)
        sub.close(sub_close_options=0, close_sub_queue=True)
        self.assertEqual(data, msg)

    def test_pubsub_admin_managed(self):
        topic_string = py23byte(self.topic_string_template.format(type="ADMIN", destination="MANAGED", durable="DURABLE"))
        subname = py23byte(self.subname_template.format(type="Admin", destination="Managed", durable="Durable"))
        msg = py23byte(self.msg_template.format(topic_string=topic_string))
        queue_name = py23byte(self.queue_name_template.format(type="ADMIN", durable="DURABLE"))
        sub_desc = self.get_subscription_descriptor(subname, topic_string, pymqi.CMQC.MQSO_RESUME)

        # register Subscription
        self.create_admin_subscription(pymqi.CMQC.MQDC_MANAGED, subname, queue_name, topic_string)
        sub = pymqi.Subscription(self.qmgr)
        self.sub_desc_list = [(sub, sub_desc, None)]
        sub.sub(sub_desc=sub_desc)
        # publish (put)
        self.pub(msg, topic_string)

        get_opts = self.create_get_opts()
        data = sub.get(None, pymqi.md(), get_opts)

        sub.close(sub_close_options=0, close_sub_queue=True)
        self.assertEqual(data, msg)

    def test_pubsub_api_provided_durable(self):
        topic_string = py23byte(self.topic_string_template.format(type="API", destination="PROVIDED", durable="DURABLE"))
        subname = py23byte(self.subname_template.format(type="Api", destination="Provided", durable="Durable"))
        msg = py23byte(self.msg_template.format(topic_string=topic_string))
        sub_desc = self.get_subscription_descriptor(subname, topic_string,
                                                    pymqi.CMQC.MQSO_CREATE + pymqi.CMQC.MQSO_DURABLE)
        queue_name = py23byte(self.queue_name_template.format(type="API", durable="DURABLE"))
        self.create_queue(queue_name)

        # create queue
        openOpts = pymqi.CMQC.MQOO_INPUT_AS_Q_DEF
        sub_queue = pymqi.Queue(self.qmgr, queue_name, openOpts)
        # register Subscription
        sub = self.create_api_subscription()
        self.sub_desc_list = [(sub, sub_desc, queue_name)]
        sub.sub(sub_desc=sub_desc, sub_queue=sub_queue)
        # publish (put)
        self.pub(msg, topic_string)

        get_opts = self.create_get_opts()
        data = sub.get(None, pymqi.md(), get_opts)

        sub.close(sub_close_options=0, close_sub_queue=True)
        self.assertEqual(data, msg)

    def test_pubsub_api_provided_non_durable(self):
        topic_string = py23byte(self.topic_string_template.format(type="API", destination="PROVIDED", durable="NON DURABLE"))
        subname = py23byte(self.subname_template.format(type="Api", destination="Provided", durable="None Durable"))
        msg = py23byte(self.msg_template.format(topic_string=topic_string))
        sub_desc = self.get_subscription_descriptor(subname, topic_string,
                                                    pymqi.CMQC.MQSO_CREATE)
        queue_name = py23byte(self.queue_name_template.format(type="API", durable="NON_DURABLE"))
        # create queue
        self.create_queue(queue_name)
        openOpts = pymqi.CMQC.MQOO_INPUT_AS_Q_DEF
        sub_queue = pymqi.Queue(self.qmgr, queue_name, openOpts)
        # register Subscription
        sub = self.create_api_subscription()
        sub.sub(sub_desc=sub_desc, sub_queue=sub_queue)
        self.sub_desc_list = [(sub, sub_desc, queue_name)]
        # publish (put)
        self.pub(msg, topic_string)
        get_opts = self.create_get_opts()
        data = sub.get(None, pymqi.md(), get_opts)
        sub.close(sub_close_options=0, close_sub_queue=True)
        self.assertEqual(data, msg)
        
    def test_pubsub_admin_provided(self):
        topic_string = py23byte(self.topic_string_template.format(type="ADMIN", destination="PROVIDED", durable="DURABLE"))
        subname = py23byte(self.subname_template.format(type="Admin", destination="Provided", durable="Durable"))
        msg = py23byte(self.msg_template.format(topic_string=topic_string))
        queue_name = py23byte(self.queue_name_template.format(type="ADMIN", durable="DURABLE"))
        sub_desc = self.get_subscription_descriptor(subname, topic_string, pymqi.CMQC.MQSO_RESUME)
        # create queue
        self.create_queue(queue_name)
        openOpts = pymqi.CMQC.MQOO_INPUT_AS_Q_DEF
        sub_queue = pymqi.Queue(self.qmgr, queue_name, openOpts)

        # register Subscription
        self.create_admin_subscription(pymqi.CMQC.MQDC_PROVIDED, subname, queue_name, topic_string)
        sub = pymqi.Subscription(self.qmgr)
        
        sub.sub(sub_desc=sub_desc, sub_queue=sub_queue)
        self.sub_desc_list = [(sub, sub_desc, queue_name)]
        # publish (put)
        self.pub(msg, topic_string)

        get_opts = self.create_get_opts()
        data = sub.get(None, pymqi.md(), get_opts)

        sub.close(sub_close_options=0, close_sub_queue=True)
        self.assertEqual(data, msg)

    def test_pubsub_already_exists(self):
        """Trying to register an already existing subscription should raise an exception.
        """
        topic_string = py23byte(self.topic_string_template.format(type="API", destination="MANAGED", durable="DURABLE"))
        subname = py23byte(self.subname_template.format(type="Api", destination="Managed", durable="Durable"))
        msg = py23byte(self.msg_template.format(topic_string=topic_string))
        # define a list self.sub_desc_list of subscription definitions so tearDown() can find it
        sub_desc = self.get_subscription_descriptor(subname, topic_string,
                                                    pymqi.CMQC.MQSO_CREATE + pymqi.CMQC.MQSO_DURABLE + pymqi.CMQC.MQSO_MANAGED)
        # register Subscription
        sub = self.create_api_subscription()
        # this modifies the subscription descriptor
        sub.sub(sub_desc=sub_desc)
        sub = self.create_api_subscription()
        self.sub_desc_list = [(sub, sub_desc, None)]
        with self.assertRaises(pymqi.MQMIError) as cm:
            # create a new subscription descriptor
            # but do not add it to the list self.sub_desc_list
            # because tearDown() would try to delete the subscription
            # and fail because this registration will not succeed
            sub_desc = self.get_subscription_descriptor(subname, topic_string,
                            pymqi.CMQC.MQSO_CREATE + pymqi.CMQC.MQSO_DURABLE + pymqi.CMQC.MQSO_MANAGED)
            sub.sub(sub_desc=sub_desc)
        # Exception should be
        # FAILED: MQRC_SUB_ALREADY_EXISTS
        self.assertEqual(cm.exception.reason, pymqi.CMQC.MQRC_SUB_ALREADY_EXISTS)

    def test_pubsub_encoding(self):
        """Test Encoding in managed and non durable subscription.
        """
        topic_string = py23byte(self.topic_string_template.format(type="API", destination="MANAGED", durable="NON DURABLE"))
        subname = py23byte(self.subname_template.format(type="Api", destination="Managed", durable="Non Durable"))
        messages = ["ascii", unicode("Euro sign: €", "iso-8859-15"), unicode("Umläut", "iso-8859-15"), unicodedata.lookup("INFINITY")]

        md = pymqi.md()
        # setting this means the message is entirely character data
        # md.Format = pymqi.CMQC.MQFMT_STRING
        # default
        # md.CodedCharSetId = pymqi.CMQC.MQCCSI_Q_MGR
        # UTF-8
        md.CodedCharSetId = 1208
        # UCS-2
        # md.CodedCharSetId = 1200
        # ISO-8859-1
        # md.CodedCharSetId = 819
        # ASCII
        # md.CodedCharSetId = 437

        # do not add the subscription to the list,
        # because tearDown() does not have to delete the subscription (in this non durable case)
        sub_desc = self.get_subscription_descriptor(subname, topic_string,
                                                    pymqi.CMQC.MQSO_CREATE + pymqi.CMQC.MQSO_MANAGED)
        # register Subscription
        sub = self.create_api_subscription()
        sub.sub(sub_desc=sub_desc)
        # publish (put)
        for msg in messages:
            self.pub(msg.encode("utf-8"), topic_string, md)

        get_opts = self.create_get_opts()
        get_opts["Options"] += pymqi.CMQC.MQGMO_CONVERT
        # md.CodedCharSetId = 819
        # md.CodedCharSetId = 437
        for msg in messages:
            # clear md for re-use
            md.MsgId = pymqi.CMQC.MQMI_NONE
            md.CorrelId = pymqi.CMQC.MQCI_NONE
            md.GroupId  = pymqi.CMQC.MQGI_NONE    
            # md.CodedCharSetId = 819
            data = sub.get(None, md, get_opts)
            self.assertEqual(unicode(data, "utf-8"), msg)
        sub.close(sub_close_options=0, close_sub_queue=True)


if __name__ == "__main__":
    unittest.main()
