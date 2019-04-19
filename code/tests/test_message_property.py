"""Test setting message properties and getting its values
"""
import unittest

import config
import env
import utils

import pymqi

class TestMP(unittest.TestCase):
    def setUp(self):

        self.msg_prop_name = utils.py3str2bytes("test_name")
        self.msg_prop_value = utils.py3str2bytes("test_valuetest_valuetest_valuetest_valuetest_value")

        # max length of queue names is 48 characters
        self.queue_name = "{prefix}.MSG.PROP.QUEUE".format(prefix=config.MQ.QUEUE.PREFIX)
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
        pcf = pymqi.PCFExecute(self.qmgr)
        pcf.MQCMD_CREATE_Q(args)
        pcf.disconnect

    def delete_queue(self, queue_name):
        
        pcf = pymqi.PCFExecute(self.qmgr)
        args = {pymqi.CMQC.MQCA_Q_NAME: utils.py3str2bytes(queue_name),
                pymqi.CMQCFC.MQIACF_PURGE: pymqi.CMQCFC.MQPO_YES}
        pcf.MQCMD_DELETE_Q(args)
    
    def workWithProp(self):
        messageHandle_get = None
        try:
            cmho_put = pymqi.CMHO()
            messageHandle_put = pymqi.MessageHandle(self.qmgr, cmho_put)
            messageHandle_put.properties.set(self.msg_prop_name, self.msg_prop_value)
            
            pmo = pymqi.PMO()
            pmo.OriginalMsgHandle = messageHandle_put.msg_handle

            md_put = pymqi.MD()

            queue_put = pymqi.Queue(self.qmgr, self.queue_name, pymqi.CMQC.MQOO_OUTPUT)
            queue_put.put(b'', md_put, pmo)

            queue_put.close()


            gmo = pymqi.GMO()
            gmo.Options = pymqi.CMQC.MQGMO_NO_WAIT | pymqi.CMQC.MQGMO_PROPERTIES_IN_HANDLE 
            gmo.MatchOptions = pymqi.CMQC.MQMO_MATCH_MSG_ID

            cmho_get = pymqi.CMHO()
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

############################################################################
#
# Real Tests start here
#
############################################################################

    def test_message_properties_short(self):
        messageHandle_get = self.workWithProp()

        try:
            messageHandle_get.properties.get(self.msg_prop_name, max_value_length=len(self.msg_prop_value)//2)
        except pymqi.MQMIError as e:
            self.assertEqual(e.reason, pymqi.CMQC.MQRC_PROPERTY_VALUE_TOO_BIG, e)

    def test_message_properties_full(self):
        messageHandle_get = self.workWithProp()

        value = messageHandle_get.properties.get(self.msg_prop_name, max_value_length=len(self.msg_prop_value))
        
        self.assertEqual(self.msg_prop_value, value)

if __name__ == "__main__":
    unittest.main()
