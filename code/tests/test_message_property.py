"""Test setting message properties and getting its values
"""
import unittest

import config
import utils

import pymqi

class TestMP(unittest.TestCase):
    def setUp(self):

        self.msg_prop_name = b"test_name"

        self.msg_prop_value_str = "test_valuetest_valuetest_valuetest_valuetest_value"
        self.msg_prop_value_bytes = b"test_valuetest_valuetest_valuetest_valuetest_value"
        self.msg_prop_value_bool = True
        self.msg_prop_value_int8 = -127
        self.msg_prop_value_int16 = -32768
        self.msg_prop_value_int32 = -2147483647
        self.msg_prop_value_int64 = -9223372036854775808
        self.msg_prop_value_float32 = 1.1754943508222875e-38
        self.msg_prop_value_float64 = 2.2250738585072014e-308



        # max length of queue names is 48 characters
        self.queue_name = "{prefix}MSG.PROP.QUEUE".format(prefix=config.MQ.QUEUE.PREFIX)
        self.queue_manager = config.MQ.QM.NAME
        self.channel = config.MQ.QM.CHANNEL
        self.host = config.MQ.QM.HOST
        self.port = config.MQ.QM.PORT
        self.user = config.MQ.QM.USER
        self.password = config.MQ.QM.PASSWORD

        self.conn_info = "{0}({1})".format(self.host, self.port)

        self.qmgr = pymqi.QueueManager(None)
        self.qmgr.connectTCPClient(self.queue_manager, pymqi.CD(), self.channel, self.conn_info, self.user, self.password)

        self.create_queue(self.queue_name)

    def tearDown(self):
        """Delete the created objects.
        """
        if self.queue_name:
            self.delete_queue(self.queue_name)
        self.qmgr.disconnect()

    def create_queue(self, queue_name):
        queue_type = pymqi.CMQC.MQQT_LOCAL
        max_depth = 5000

        args = {pymqi.CMQC.MQCA_Q_NAME: utils.py3str2bytes(queue_name),
                pymqi.CMQC.MQIA_Q_TYPE: queue_type,
                pymqi.CMQC.MQIA_MAX_Q_DEPTH: max_depth,
                pymqi.CMQCFC.MQIACF_REPLACE: pymqi.CMQCFC.MQRP_YES}
        pcf = pymqi.PCFExecute(self.qmgr, response_wait_interval=120000)
        pcf.MQCMD_CREATE_Q(args)
        pcf.disconnect

    def delete_queue(self, queue_name):

        pcf = pymqi.PCFExecute(self.qmgr, response_wait_interval=120000)
        args = {pymqi.CMQC.MQCA_Q_NAME: utils.py3str2bytes(queue_name),
                pymqi.CMQCFC.MQIACF_PURGE: pymqi.CMQCFC.MQPO_YES}
        pcf.MQCMD_DELETE_Q(args)

    def get_value_length(self, property_type, property_value = ''):
        value_length = 0
        if property_type == pymqi.CMQC.MQTYPE_BOOLEAN:
            value_length = 4
        elif property_type == pymqi.CMQC.MQTYPE_BYTE_STRING:
            value_length=len(property_value)
        elif property_type == pymqi.CMQC.MQTYPE_INT8:
            value_length = 1
        elif property_type == pymqi.CMQC.MQTYPE_INT16:
            value_length = 2
        elif property_type == pymqi.CMQC.MQTYPE_INT32:
            value_length = 4
        elif property_type == pymqi.CMQC.MQTYPE_INT64:
            value_length = 8
        elif property_type == pymqi.CMQC.MQTYPE_FLOAT32:
            value_length = 4
        elif property_type == pymqi.CMQC.MQTYPE_FLOAT64:
            value_length = 8
        elif property_type == pymqi.CMQC.MQTYPE_STRING:
            value_length=len(property_value)
        elif property_type == pymqi.CMQC.MQTYPE_NULL:
            value_length == 0

        return value_length

    def work_with_property(self, property_value, property_type):
        messageHandle_get = None
        queue_get = None
        queue_put = None
        try:

            value_length = self.get_value_length(property_type, property_value)

            cmho_put = pymqi.CMHO()
            messageHandle_put = pymqi.MessageHandle(self.qmgr, cmho_put)
            messageHandle_put.properties.set(self.msg_prop_name, property_value,
                                            value_length=value_length,
                                            property_type=property_type)

            pmo = pymqi.PMO(Version=pymqi.CMQC.MQPMO_CURRENT_VERSION)
            pmo.OriginalMsgHandle = messageHandle_put.msg_handle

            md_put = pymqi.MD(Version=pymqi.CMQC.MQMD_CURRENT_VERSION)

            queue_put = pymqi.Queue(self.qmgr, self.queue_name, pymqi.CMQC.MQOO_OUTPUT)
            queue_put.put(b'', md_put, pmo)

            queue_put.close()


            gmo = pymqi.GMO(Version=pymqi.CMQC.MQGMO_CURRENT_VERSION)
            gmo.Options = pymqi.CMQC.MQGMO_NO_WAIT | pymqi.CMQC.MQGMO_PROPERTIES_IN_HANDLE
            gmo.MatchOptions = pymqi.CMQC.MQMO_MATCH_MSG_ID

            cmho_get = pymqi.CMHO(Version=pymqi.CMQC.MQCMHO_CURRENT_VERSION)
            messageHandle_get = pymqi.MessageHandle(self.qmgr, cmho_get)
            gmo.MsgHandle = messageHandle_get.msg_handle
            md_get = pymqi.MD()
            md_get.MsgId = md_put.MsgId

            queue_get = pymqi.Queue(self.qmgr, self.queue_name, pymqi.CMQC.MQOO_INPUT_AS_Q_DEF)
            queue_get.get(None, md_get, gmo)
        finally:
            if queue_put:
                if queue_put.get_handle():
                    queue_put.close()

            if queue_get:
                if queue_get.get_handle():
                    queue_get.close()

        return messageHandle_get

    def get_property_value(self, messageHandle_get,
                           property_type=pymqi.CMQC.MQTYPE_AS_SET,
                           value_length=None,
                           property_modify=False):
        if not value_length:
            value_length = self.get_value_length(property_type)
        if property_modify:
            property_name = self.msg_prop_name*2
        else:
            property_name = self.msg_prop_name

        return messageHandle_get.properties.get(property_name,
                                                property_type=property_type,
                                                max_value_length=value_length)




############################################################################
#
# Real Tests start here
#
############################################################################

    def test_message_properties_short(self):
        messageHandle_get = self.work_with_property(self.msg_prop_value_bytes, pymqi.CMQC.MQTYPE_BYTE_STRING)

        try:
            messageHandle_get.properties.get(self.msg_prop_name, max_value_length=len(self.msg_prop_value_bytes)//2)
        except pymqi.MQMIError as e:
            self.assertEqual(e.reason, pymqi.CMQC.MQRC_PROPERTY_VALUE_TOO_BIG, e)

    def test_message_properties_byte(self):
        messageHandle_get = self.work_with_property(self.msg_prop_value_bytes, pymqi.CMQC.MQTYPE_BYTE_STRING)

        value = messageHandle_get.properties.get(self.msg_prop_name, max_value_length=len(self.msg_prop_value_bytes))

        self.assertEqual(self.msg_prop_value_bytes, value)

    def test_message_properties_str(self):
        messageHandle_get = self.work_with_property(self.msg_prop_value_str, pymqi.CMQC.MQTYPE_STRING)

        value = messageHandle_get.properties.get(self.msg_prop_name, max_value_length=len(self.msg_prop_value_str))

        self.assertEqual(self.msg_prop_value_str, value)

    def test_message_properties_bool(self):
        messageHandle_get = self.work_with_property(self.msg_prop_value_bool, pymqi.CMQC.MQTYPE_BOOLEAN)
        value = self.get_property_value(messageHandle_get)

        self.assertEqual(self.msg_prop_value_bool, value)

    def test_message_properties_int8(self):
        messageHandle_get = self.work_with_property(self.msg_prop_value_int8, pymqi.CMQC.MQTYPE_INT8)
        value = self.get_property_value(messageHandle_get)

        self.assertEqual(self.msg_prop_value_int8, value)

    def test_message_properties_int16(self):
        messageHandle_get = self.work_with_property(self.msg_prop_value_int16, pymqi.CMQC.MQTYPE_INT16)
        value = self.get_property_value(messageHandle_get)

        self.assertEqual(self.msg_prop_value_int16, value)

    def test_message_properties_int32(self):
        messageHandle_get = self.work_with_property(self.msg_prop_value_int32, pymqi.CMQC.MQTYPE_INT32)
        value = self.get_property_value(messageHandle_get)

        self.assertEqual(self.msg_prop_value_int32, value)


    def test_message_properties_int64(self):
        messageHandle_get = self.work_with_property(self.msg_prop_value_int64, pymqi.CMQC.MQTYPE_INT64)
        value = self.get_property_value(messageHandle_get)

        self.assertEqual(self.msg_prop_value_int64, value)

    def test_message_properties_float32(self):
        messageHandle_get = self.work_with_property(self.msg_prop_value_float32, pymqi.CMQC.MQTYPE_FLOAT32)
        value = self.get_property_value(messageHandle_get)

        self.assertEqual(self.msg_prop_value_float32, value)

    def test_message_properties_float64(self):
        messageHandle_get = self.work_with_property(self.msg_prop_value_float64, pymqi.CMQC.MQTYPE_FLOAT64)
        value = self.get_property_value(messageHandle_get)

        self.assertEqual(self.msg_prop_value_float64, value)

    def test_message_properties_null(self):
        messageHandle_get = self.work_with_property(None, pymqi.CMQC.MQTYPE_NULL)
        value = self.get_property_value(messageHandle_get)

        self.assertEqual(None, value)

    def test_message_properties_nonexist(self):
        messageHandle_get = self.work_with_property(None, pymqi.CMQC.MQTYPE_NULL)
        try:
            value = self.get_property_value(messageHandle_get, property_modify=True)

        except pymqi.MQMIError as e:
            self.assertEqual(e.reason, pymqi.CMQC.MQRC_PROPERTY_NOT_AVAILABLE, e)



if __name__ == "__main__":
    unittest.main()
