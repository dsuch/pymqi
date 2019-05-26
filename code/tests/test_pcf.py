"""Test PCF usage
"""

import unittest

import config
import utils
import env

import pymqi

class TestPCF(unittest.TestCase):
    def setUp(self):
        # max length of queue names is 48 characters
        self.queue_name = "{prefix}PCF.QUEUE".format(prefix=config.MQ.QUEUE.PREFIX)
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
                pymqi.CMQC.MQCA_Q_DESC: utils.py3str2bytes('PCF testing'),
                pymqi.CMQCFC.MQIACF_REPLACE: pymqi.CMQCFC.MQRP_YES}
        pcf = pymqi.PCFExecute(self.qmgr)
        pcf.MQCMD_CREATE_Q(args)
        pcf.disconnect

    def delete_queue(self, queue_name):

        pcf = pymqi.PCFExecute(self.qmgr)
        args = {pymqi.CMQC.MQCA_Q_NAME: utils.py3str2bytes(queue_name),
                pymqi.CMQCFC.MQIACF_PURGE: pymqi.CMQCFC.MQPO_YES}
        pcf.MQCMD_DELETE_Q(args)
        pcf.disconnect

    def test_object_inquire_multiple_attributes(self):
        attrs = {
            pymqi.CMQC.MQCA_Q_NAME : utils.py3str2bytes(self.queue_name),
            pymqi.CMQC.MQIA_Q_TYPE : pymqi.CMQC.MQQT_LOCAL,
            pymqi.CMQCFC.MQIACF_Q_ATTRS : [pymqi.CMQC.MQIA_CURRENT_Q_DEPTH, pymqi.CMQC.MQCA_Q_DESC]
            }

        pcf = pymqi.PCFExecute(self.qmgr)
        results = pcf.MQCMD_INQUIRE_Q(attrs)
        pcf.disconnect
        
        queue_inquired = False
        for result in results:
            if result.get(pymqi.CMQC.MQCA_Q_NAME).decode().strip() == self.queue_name:
                if pymqi.CMQC.MQIA_CURRENT_Q_DEPTH in result and pymqi.CMQC.MQCA_Q_DESC in result:
                    queue_inquired = True
        
        self.assertEqual(True, queue_inquired)

if __name__ == "__main__":
    unittest.main()        
