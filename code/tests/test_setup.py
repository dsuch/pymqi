"""Setup tests environment."""
import unittest

import config
import utils

import pymqi

class Tests(unittest.TestCase):
    """Setup and tearsdown tests environment."""

    def setUp(self):
        """Setup tests environmet.
        Configuration for setup provided by config.py
        Creates connection `self.qmgr` to Queue Manager `self.queue_manager`
        and creates queue `self.queue_name`
        """
        # max length of queue names is 48 characters
        self.queue_name = "{prefix}MSG.QUEUE".format(prefix=config.MQ.QUEUE.PREFIX)
        self.queue_manager = config.MQ.QM.NAME
        self.channel = config.MQ.QM.CHANNEL
        self.host = config.MQ.QM.HOST
        self.port = config.MQ.QM.PORT
        self.user = config.MQ.QM.USER
        self.password = config.MQ.QM.PASSWORD

        self.conn_info = "{0}({1})".format(self.host, self.port)

        self.qmgr = pymqi.QueueManager(None)
        self.qmgr.connectTCPClient(self.queue_manager, pymqi.CD(), self.channel, self.conn_info, self.user, self.password)

    def tearDown(self):
        """Clear test environment."""
        self.qmgr.disconnect()

    def create_queue(self, queue_name, max_depth=5000):
        queue_type = pymqi.CMQC.MQQT_LOCAL

        args = {pymqi.CMQC.MQCA_Q_NAME: utils.py3str2bytes(queue_name),
                pymqi.CMQC.MQIA_Q_TYPE: queue_type,
                pymqi.CMQC.MQIA_MAX_Q_DEPTH: max_depth,
                pymqi.CMQCFC.MQIACF_REPLACE: pymqi.CMQCFC.MQRP_YES}
        pcf = pymqi.PCFExecute(self.qmgr)
        pcf.MQCMD_CREATE_Q(args)

    def delete_queue(self, queue_name):
        pcf = pymqi.PCFExecute(self.qmgr)
        args = {pymqi.CMQC.MQCA_Q_NAME: utils.py3str2bytes(queue_name),
                pymqi.CMQCFC.MQIACF_PURGE: pymqi.CMQCFC.MQPO_YES}
        pcf.MQCMD_DELETE_Q(args)